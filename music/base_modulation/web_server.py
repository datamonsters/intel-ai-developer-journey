'''
Basic REST API wrapper for transformation script
Alexey Kalinin, 2017

Usage:
python3 web_server.py

Request format
GET request to http://127.0.0.1:8083/
{
    "method": "midi",
    "emotion": "EMOTION_NAME"
}
Example:
http://127.0.0.1:8083/?method=midi&emotion=AWE

Response format
On request we select random melody from list, perform transformation and return it in JSON format.
MIDI file can be returned via link or as base64 representation within JSON response, see example below.

Return JSON string:
{
    "status": "[1,0]",
    "message": "info about transformation or error message",
    "file": "link to file/base64 representation",
}

Examples of responses:
On success:
- for link return:
{
    "status": "1",
    "message": "Transformation of Brother John to AWE",
    "file": "http://192.168.1.45:8082/transformed/Brother_John_AWE_64c1551a-79c6-11e7-b3c5-bcaec56d64f1.mid"
}
link will be deleted after some period of time.

- for base64 return:
{
    "status": "1",
    "message": "Transformation of Brother John to AWE",
    "file": "b'BFAI4zgDwAiAD/LwA.....................'"
}

On wrong method in request:
{
    "status": "0", "message": "Wrong method", "file": "None"
}

On wrong request format (missing method or emotion value)
{
    "status": "0", "message": "Wrong request", "file": "None"
}

On request for unsupported emotion:
{
    "status": "0", "message": "Wrong emotion, available: ANXIETY, AWE, JOY, SADNESS, DETERMINATION", "file": "None"
}


Edit HOST and PORT vars according to your network
'''

HOST='192.168.1.45'
PORT=8082

SRC_MIDI_PATH='../base_melodies'
TARGET_MIDI_PATH='./transformed'

import threading
import string
import random
import os
import glob
import base64
from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from emotransform import EMOTIONS
from emotransform import transform
from emotransform import nn_harmonize

#URL for link name in response
BASE_URL='http://{0}:{1}/'.format(HOST,PORT)
#return midi as link or base64
RETURN_LINK=True

MELODIES=list();
respons_tmpl = string.Template('''
{
      "status": "$status",
      "message": "$message",
      "file": "$file"
}
''')

class midiRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        query = parse.parse_qs(self.path[2:])
        print(query)

        if (len(query) == 0):
            # return file
            try:
                midiFile = open(self.path[1:],'rb')

                self.send_response(200)
                self.send_header('Content-type','application/midi')
                self.end_headers()

                self.wfile.write(midiFile.read())
                midiFile.close()

                #message = self.path[1:];
                #self.wfile.write(bytes(message, 'utf8'))

            except IOError:
                self.wfile.write(bytes(respons_tmpl.substitute(status='0', message='File Not Found', file=self.path), 'utf8') )

        else:
            # return json-response
            self.send_response(200)
            self.send_header('Content-type','text/json')
            self.end_headers()

            # leave only first value for each key in dict
            query = {key: query[key][0] for key in query}
            message = queryHandler(query)
            self.wfile.write(bytes(message, "utf8"))
        return


def queryHandler(query):
    print(query)
    rez_string = ''

    #some basic value checking
    if (not ('method' in query) or not ('emotion' in query) ):
        return respons_tmpl.substitute(status='0', message='Wrong request', file='None')

    if (query['method'] == 'midi'):
        # check if we support this transformation
        if (not query['emotion'] in EMOTIONS):
            prep_mess = 'Wrong emotion, available: '+', '.join(EMOTIONS)
            return respons_tmpl.substitute(status='0', message=prep_mess, file='None')

        # select random melody from available list
        melody_file = random.choice(MELODIES)
        # make transform
        # perform emotion modulation
        modulated_file_name, _ = transform(SRC_MIDI_PATH + '/' + melody_file, query['emotion'], TARGET_MIDI_PATH)
        # perform neural network harmonization via BachBot
        nn_modulated_file_name, _ = nn_harmonize(modulated_file_name, TARGET_MIDI_PATH, query['emotion'])

        # make file name more nice for message
        (filename, _) = melody_file.split('.')
        filename = filename.replace('_',' ')
        prep_mess = 'Transformation of '+filename+' to ' + query['emotion']

        return_string = ''
        if (RETURN_LINK):
            return_string = parse.urljoin(BASE_URL, TARGET_MIDI_PATH + '/' + nn_modulated_file_name)
        else:
            fm = open(TARGET_MIDI_PATH + '/' + nn_modulated_file_name, 'rb')
            return_string = base64.b64encode(fm.read())

        rez_string = respons_tmpl.substitute(status='1', message=prep_mess, file=return_string)

    else:
        rez_string = respons_tmpl.substitute(status='0', message='Wrong method', file='None')

    return rez_string

def runWebServer():
    try:
        server_address = ('', PORT)
        httpd = HTTPServer(server_address, midiRequestHandler)
        print("Web server started on {0}".format(server_address))
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

if __name__ == "__main__":
    MELODIES = glob.glob1(SRC_MIDI_PATH, '*.xml')
    print(MELODIES)
    if (not os.path.exists(TARGET_MIDI_PATH)): os.makedirs(TARGET_MIDI_PATH)
    try:
        webThread = threading.Thread(target=runWebServer)
        webThread.start()
    except KeyboardInterrupt:
        web_server.server_close()

