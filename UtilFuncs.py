import pyttsx3
#import speech_recognition as sr
#import datetime
#import webbrowser
#import os


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[0].id)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()
#speak("Hello sir how are you?")

'''
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')#, show_all=True)
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Say that again please")
            return "None"
        return query



def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")




def TakeImages():       #capture face images from live webcam footage
    Id = (txt.get())
    name = (txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = 'haarcascade_frontalface_default.xml'
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while True:
            ret,img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
                sampleNum = sampleNum+1
                cv2.imwrite("TrainingImages\ "+name+"."+Id+'.'+str(sampleNum) + ".jpg", gray[y:y+h,x:x+h])
                cv2.imshow('Frame', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 60:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = 'Images Saved for id: '+Id+' Name: '+name
        row = [Id, name]
        with open('StudentDetails\studentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text=res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text = res)
        elif(name.isalpha()):
            res = "Enter numeric ID"
            message.configure(text=res)
'''
