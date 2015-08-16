from flask import Flask
import speech_recognition as sr
import socket 

import flask 

app = Flask(__name__)

@app.route('/')
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:                # use the default microphone as the audio source
        r.adjust_for_ambient_noise(source)         # listen for 1 second to calibrate the energy threshold for ambient noise levels
        print("Done calibrating")
        audio = r.listen(source)                   # now when we listen, the energy threshold is already set to a good value, and we can reliably catch speech right away
    res = None
    try:
        res = r.recognize(audio)
        print("You said: " + res)                  # recognize speech using Google Speech Recognition
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio")
    
    result = {}
    result['result'] = res
    return flask.jsonify(**result)
    

if __name__ == '__main__':
    app.debug=True
    app.run(host=socket.gethostbyname(socket.gethostname()), port=5555)
    
    
