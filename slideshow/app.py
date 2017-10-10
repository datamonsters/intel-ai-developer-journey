from shutil import copyfile
import time
import requests
import urllib
import random
import json
#from PIL import Image


from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)
from werkzeug import secure_filename
import os
import string
from random import sample, choice

MUSIC_SERVICE_URL = 'https://lab.datamonsters.co/music-service/'
EMOTIONS_SERVICE_URL = 'http://13.90.212.221:9000/predict'

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)


app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'JPG', 'JPEG'])
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    if endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    if endpoint == 'data_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'upload', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)

@app.route('/data/<path:filename>')
def data_static(filename):
    return send_from_directory(app.root_path + '/upload/', filename)

@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)

def generate_session():
    '''
    Generates a sequence of symbols to name a slideshow
    '''
    chars = string.letters + string.digits
    length = 8
    return ''.join(choice(chars) for _ in range(length))

@app.route('/')
def index():
    newsession = generate_session()
    # generating a new session, repeating if exists
    while os.path.exists(os.path.join(basedir, 'upload/'+newsession+'')):
        newsession = generate_session()
    return render_template('index.html', session_name = newsession)

@app.route('/show/<path:session>')
def show_page(session):
    #check if music is already generated
    for x in range(1, 6):
        music_path = os.path.join(basedir, 'upload/' + session + '/' + str(x) + '.mid') 
        if not os.path.exists(music_path): 
            emotion = get_emotion(os.path.join(basedir, 'upload/' + session + '/' + str(x) + '.jpg')) 
            generate_music(emotion, session, x)
            time.sleep(1)
    return render_template('show.html', session_name = session)

def generate_music(emotion, session, num):
    url = MUSIC_SERVICE_URL + '?method=midi&emotion='+emotion
    resp = requests.get(url=url)
    data = json.loads(resp.text) 
    urllib.urlretrieve(data['file'], os.path.join(basedir, 'upload/' + session + '/' + str(num) + '.mid'))

def get_emotion(file_path):
    image_file = {'data': ('x.jpg', open(file_path, 'rb'))}
    r = requests.post(EMOTIONS_SERVICE_URL, files=image_file)
    data = json.loads(r.text)
    v = data[0][0]
    print data
    positive = ['ANXIETY', 'AWE', 'JOY']
    negative = ['SADNESS', 'DETERMINATION']
    if v == 'Negative' :
        print v
        return random.choice(negative)
    else :
        print v 
        return random.choice(positive)


@app.route('/uploadajax/<path:session>/<path:number>', methods=['POST'])
def upldfile(session, number):
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        dirname = os.path.join(basedir, 'upload/'+session+'/')
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        updir = os.path.join(dirname)
        for f in files:
            if f and allowed_file(f.filename):
                filename =  number + ".jpg"
                f.save(os.path.join(updir, filename))
                #filenameOriginal =  filename
                #f.save(os.path.join(updir, filenameOriginal))
                #filename =  number + "t.jpg"
                #size = 500, 500
                #try:
                #    im = Image.open(os.path.join(updir, filenameOriginal))
                #    
                #    im.thumbnail(size, Image.ANTIALIAS)
                #    im.save(os.path.join(updir,filename), "JPEG")                    
                #except IOError:
                #    print "cannot create thumbnail for '%s'" % infile
                            
                file_size = os.path.getsize(os.path.join(updir, filename))
            else:
                app.logger.info('ext name error')
                return jsonify(error='ext name error')
        return jsonify(name=filename, size=file_size)


class ReverseProxied(object):
    '''
    Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

class PrefixMiddleware(object):

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]


app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/slideshow-music')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True) 
