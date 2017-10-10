# Application Deveopment

## Idea
The goal of applicaion is to show users that AI tecnologies is not about soulless machines. Let's help people share their emotions. All of you have a lot of photos envokeing emotions that can be shared by means of music. 
Looking ahead, you can find running application here: [lab.datamonsters.co/slideshow-music/](https://lab.datamonsters.co/slideshow-music/)

## Defining User Stories
Let's write down userstories covering future application:
- User can select 5 photos from his computer (using upload dialog or drag-n-drop)
- User can upload photots to make the app generate a slideshow
- The app calls API to extract emotions from photots
- The app calls API to generate a music based on emotions
- User can view the slideshow with listening generated music
- User can share the slideshow with music in social networks

## Technologies
As the reader already familiar with Python so it seems to be the best choise as programming language.
The simpliest framework to build web applications on Python is [Flask](http://flask.pocoo.org/).
In role of seed project one can take something with already implemented file upload, for example [this one](https://github.com/moremorefor/flask-fileupload-dropzonejs) with Flask + [Dropzone.js](http://www.dropzonejs.com/) stack. As music generation service returns midi files the app will use [MIDIjs](https://github.com/mudcube/MIDI.js/) to play it.

## Developing the app
Based on user stories the app architecture will consist of 4 parts:
- Web client
- Web app server
- Remote image processing service
- Remote music generation service

Web client will be presented by 2 views:
- Photo uploading view
- Slideshow view, that will be sharable

For each view Flask app needs methods to be implemented and also one methon to upload images. 
Index page will provide only upload form. Let's upload method as is in example and implement slideshow generation in method **show**. Here the system calls remote API to extract emotions and generate MIDIs with music:

```Python
@app.route('/show/<path:session>')
def show_page(session):
    #check if music is already generated
    for x in range(1, 6):
        music_path = os.path.join(basedir, 'upload/' + session + '/' + str(x) + '.mid')
        if not os.path.exists(music_path):
            emotion = get_emotion(os.path.join(basedir, 'upload/' + session + '/' + str(x) + '.jpg'))
            generate_music(emotion, session, x)
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
```

To provide diversity there are several positive and negative emotions that are randomly selected to generate music.

On the client side you just need to implement a slideshow with playing MIDI.
Slideshow implementations can be found on CodePan. [Here is](https://codepen.io/gabrieleromanato/pen/dImly) one of them.

## Deployment
You can get full source code of the app [here](https://github.com/datamonsters/intel-ai-developer-journey/tree/master/slideshow). Or just checkout it 
```bash
git checkout git@github.com:datamonsters/intel-slideshow-music.git
cd intel-ai-developer-journey/slideshow
```
Then you should replace urls of music and emotions services in app.py with your services urls.
```python
MUSIC_SERVICE_URL = 'https://lab.datamonsters.co/music-service/'
EMOTIONS_SERVICE_URL = 'http://13.90.212.221:9000/predict'
```
To launch the server just type
```bash
cd intel-slideshow-music
pip install -r requirements.txt
export FLASK_APP=app
flask run
```
Then open in your browser http://localhost:5000/slideshow-music
