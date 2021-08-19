import tkinter as tk
from PIL import ImageTk, Image
#from tkinter.ttk import *
import os, cv2
import numpy as np
from PIL import Image, ImageTk
import sqlite3
import datetime
import time
import ManageStudents as ms
import UtilFuncs as util

def manageStudentResponse():  
    ob = ms.ManageStudents()
    #ob.createGUI()



#Returns the images in 2D matrix form and ID of the images
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    print("Faces:")
    print(faces)
    print("IDs:")
    print(Ids)
    return faces,Ids


#To train the model
def trainSystem():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = 'haarcascade_frontalface_default.xml'
    detector = cv2.CascadeClassifier(harcascadePath)
    faces,Ids = getImagesAndLabels("TrainingImages")
    recognizer.train(faces, np.array(Ids))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    print("Training Complete")
    #res = "Training Done"#"Image Trained"+",".join(str(f) for f in Ids)
    #message2.configure(text = res)




#to check student_info table is empty or not
def tableIsEmpty():
    con = sqlite3.connect('Database.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM student_info")
    num = cursor.fetchall()
    if(num == []):
        #print("Return True")
        return True
    else:
        #print("Return False")
        return False




#to predict image id
#def predictImageId():
    

#For TrackImage Button
def TrackImages():
    conn = sqlite3.connect('Database.db')
    count = 1
    aa = ""
    Id = ""
    dept = ""
    found = False
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = 'haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    #df = pd.read_csv("StudentDetails\studentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #col_names = ['Id', 'name', 'dept', 'date', 'time']
    #attendance = pd.DataFrame(columns = col_names)
    
    while found == False:
        ret,im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(im, (x,y), (x+w, y+h), (255,0,0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                if tableIsEmpty():
                    speak("Student info database is empty. Cant Predict!")
                    conn.close()
                    cam.release()
                    cv2.destroyAllWindows()
                    return
                datas = conn.execute("SELECT name,dept FROM student_info WHERE ID="+str(Id))
                for data in datas:
                    aa = data[0]
                    dept = data[1]
                
                tt = "ID: "+str(Id)+"-Name: "+aa
                
                #attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
            else:
                Id = 'Unknown'
                tt = str(Id)
            #if conf > 75:
                #noOfFile = len(os.listdir('ImagesUnknown'))+1
                #cv2.imwrite("ImagesUnknown\Image"+str(noOfFile)+".jpg", im[y:y+h, x:x+w])
            cv2.putText(im, str(tt), (x, y+h), font, 1, (255,255,255), 2)
        #attendance = attendance.drop_duplicates(subset=['Id'], keep = 'first')
        cv2.imshow('im', im)
        if count == 1:
            util.speak("If details are matched press M. or else press escape")
            count += 1
        #key = cv2.waitKey(100)
        if cv2.waitKey(1) == ord('m'):    #checks if pressed 'm'
            found = True
            break
        elif cv2.waitKey(100) == 27:  #for escape button
            #found = False
            break
        #if cv2.waitKey(1) == ord('m'):
            #break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second = timeStamp.split(":")
    #filename = "Attendance\Attendance_" + date + "_" + Hour + '-' + Minute + '-' + Second + ".csv"
    #attendance.to_csv(filename, index=False)
    cam.release()
    cv2.destroyAllWindows()
    
    if found and str(Id) != 'Unknown':   #to get dept from Id
        #data = conn.execute("SELECT dept FROM student_info WHERE Id="+str(Id))
        #for i in data:
            #dept = i[0]
        conn.execute("INSERT INTO attendance_record(Id,name,dept,date,time) VALUES("+str(Id)+",'"+aa+"','"+dept+"','"+str(date)+"','"+str(Hour)+":"+str(Minute)+":"+Second+"')")
        conn.commit()
        util.speak("Attendance recorded successfully")
    else:
        util.speak("Sorry! No match found. Please contack to authority")
    
    conn.close()
    #res = attendance
    #message2.configure(text = res)







def main():
    mainwindow = tk.Tk()

    #create main window
    #img = ImageTk.PhotoImage(Image.open(r"D:\Python_Projects\Smart_Attendance_System\Images\AddStudent.jpg"))
    mainwindow.title("Smart Attendance System")
    mainwindow.geometry('900x600')
    #

    #For background image
    load = Image.open(r"Images\MainMenuBackground2.jpg")
    load = load.resize((900, 600), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = tk.Label(mainwindow, image=render, height = 0, width = 0)
    #img.pack(side = "bottom", fill = "both", expand = "yes")
    img.image = render
    img.place(x=-2, y=-2)
    #

    #a= tk.Label(mainwindow, text = 'Add Student', font = ('bold', 14), pady = 200).place(x = 30,y = 50)

    #for Manage Student button
    img2 = ImageTk.PhotoImage(Image.open(r"Images\AddStudent.jpg"))
    addstudent = tk.Button(mainwindow, text = "Manage Student", image = img2, command = manageStudentResponse, height = 200, width = 200)
    addstudent.place(x = 50,y = 70)
    #

    #for Train System button
    img3 = ImageTk.PhotoImage(Image.open(r"Images\Train System2 - Copy - Copy.jpg"))
    button2 = tk.Button(mainwindow, text = "Simple", image = img3, command = trainSystem, height = 200, width = 200)
    button2.place(x = 360,y = 70)
    #

    #for button3
    img4 = ImageTk.PhotoImage(Image.open(r"Images\detectFace - Copy (2) - Copy.jpg"))
    button3 = tk.Button(mainwindow, text = "Simple", image = img4, compound = tk.LEFT, command = TrackImages, height = 200, width = 200)
    button3.place(x = 650,y = 70)
    #
    
    #for upper menu
    menubar = tk.Menu(mainwindow, fg='black' )
    #For file#########################3##
    file = tk.Menu(menubar, tearoff=0)
    file.add_command(label="New")
    file.add_command(label="Open")
    file.add_command(label="Save")
    file.add_command(label="Save as")
    file.add_command(label="Close")

    file.add_separator()
    
    file.add_command(label="Exit", command=mainwindow.destroy)
    menubar.add_cascade(label="File", menu=file)
    #For file##############################

    #for Edit##############################
    edit = tk.Menu(menubar, tearoff=0)
    edit.add_command(label="Undo")
    
    edit.add_separator()  
    
    edit.add_command(label="Cut")  
    edit.add_command(label="Copy")  
    edit.add_command(label="Paste")  
    edit.add_command(label="Delete")  
    edit.add_command(label="Select All")  
      
    menubar.add_cascade(label="Edit", menu=edit) 
    #for Edit###############################
    mainwindow.config(menu=menubar)
    #for upper menu
    
    mainwindow.mainloop()

main()
