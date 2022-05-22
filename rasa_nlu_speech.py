from rasa.nlu.model import Interpreter
import speech_recognition as sr
import time
class nlu:
    rasa_model_path = "ex-mo/nlu"
    interpreter = Interpreter.load(rasa_model_path)

    def rasa_nlu(self, userIn):
        message = str(userIn).strip()
        r0ut = self.interpreter.parse(message)
        self.intent = r0ut
        return self.intent

class speech_recognize:
    def bot_listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            #print('Speak anything: ')
            while True:
                r.adjust_for_ambient_noise(source,duration=0.5)
                begin2 = time.time()
                audio = r.listen(source,timeout=8,phrase_time_limit=15)
                try:
                    text = r.recognize_google(audio,language='vi')
                    self.speech = text.format(text)
                    #print(time.time() - begin2)
                    return self.speech
                except:
                    break


