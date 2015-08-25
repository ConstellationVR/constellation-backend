from flask import Flask
import speech_recognition as sr
import socket 
import sys
import flask 

app = Flask(__name__)

@app.route('/')
def speech_to_text():
    global r, m
    # r = sr.Recognizer()
    # with sr.Microphone() as source:                # use the default microphone as the audio source
        #sys.stdout.write('\a')
        #sys.stdout.flush()
        #print("Calibrating")
        #r.adjust_for_ambient_noise(source)         # listen for 1 second to calibrate the energy threshold for ambient noise levels
        #print("Done calibrating")
        #sys.stdout.write('\a\a')
        #sys.stdout.flush()
    print("Listening")
    try:
        with m as source: audio = r.listen(source, timeout=5)                   # now when we listen, the energy threshold is already set to a good value, and we can reliably catch speech right away
        res = None
        print("Recognizing")
        res = r.recognize(audio)
        print("You said: " + res)                # recognize speech using Google Speech Recognition
        #sys.stdout.write('\a\a\a')
        #sys.stdout.flush()
    except:                            # speech is unintelligible
        print("Could not understand audio")
    
    result = {}
    result['result'] = res
    return flask.jsonify(**result)
    
    
def callback(recognizer, audio):                          # this is called from the background thread
    try:
        print("You said " + recognizer.recognize(audio))  # received audio data, now need to recognize it
    except LookupError:
        print("Oops! Didn't catch that")
        

if __name__ == '__main__':
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    m = sr.Microphone()
    # with m as source: r.adjust_for_ambient_noise(source)
    # stop_listening = r.listen_in_background(m, callback)
    
    print("Calibrating")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Done calibrating")
    
    app.debug=True
    app.run(host="0.0.0.0", port=5555)
