import tkinter as tk
import sqlite3
from tkintertable import TableCanvas, TableModel
import cv2, os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd


class ManageStudents:
    #to check student_info table is empty or not
    def tableIsEmpty(self):
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




    #to show the DB table data into tkintertable
    def show_Data_in_table(self):
        try:
            dic = {1:""}
            count = 1
            conn = sqlite3.connect('Database.db')
            data = conn.execute("SELECT * FROM student_info")
            #print(type(data))
            if self.tableIsEmpty():
                self.table = TableCanvas(tframe, read_only=True)
                self.table.show()
                #print("table is empty")
                return
            for i in data:
                #print(type(i[0]))
                dic[count] = {'Id':i[0], 'Name':i[1], 'Dept': i[2], 'Address': i[3]}
                count += 1
                #print(type(i))#(str(i[0])+"\t"+i[1])
            self.table = TableCanvas(self.tframe, data=dic, read_only=True)
            self.table.show()
        except Exception as e:
            #print("From here")
            print(e)
        finally:
            conn.close()



    #To check a variable is number or not
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False




    #For Taking Image Sample and save the student info into database
    def Take_image_sample_and_Save(self):
        try:
            #string = ""
            Id = self.id_entry.get()
            name = self.name_entry.get()
            dept = self.tkinter_variable.get()
            addr = self.addr_entry.get()
            if(name != '' and Id != '' and dept != ''):
                if(self.is_number(Id) and name.isalpha() and dept.isalpha()):
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
                            #string = string + name+"."+Id+'.'+str(sampleNum) + ".jpg,"
                            cv2.imwrite("TrainingImages\ "+name+"."+Id+'.'+str(sampleNum) + ".jpg", gray[y:y+h,x:x+h])
                            cv2.imshow('Frame', img)
                        if cv2.waitKey(100) & 0xFF == ord('q'):
                            break
                        elif sampleNum > 59:
                            break
                    cam.release()
                    cv2.destroyAllWindows()
                    #res = 'Images Saved for id: '+Id+' Name: '+name
                    #s = "INSERT INTO student_info (Id,name,dept,address) VALUES("+Id+",'"+name+"','"+dept+"','"+addr+"')"
                    s = "INSERT INTO student_info (Id,name,dept,address) VALUES(?,?,?,?)"
                    #print(s)
                    conn = sqlite3.connect('Database.db')
                    conn.execute(s,(Id,name,dept,addr))
                    conn.commit()
                    conn.close()
                    print("data inserted successfully")
                    self.show_Data_in_table()
                    #message.configure(text=res)
                else:
                    if(self.is_number(Id)):
                        print("Enter Alphabetical Name")
                    elif(name.isalpha()):
                        print("Enter numeric ID")
            else:
                print("Name, Id and dept is mandetory")
        except Exception as e:
            print(e)
    #For Taking Image Sample and save the student info into database




    #To create the GUI window
    def __init__(self):#createGUI(self):
        #For the main window
        self.window = tk.Tk()
        self.window.title("Smart Attendance System")
        self.window.geometry('1100x650')
        self.window.configure(background='gray')
        
        #to place the table into the label
        self.tframe = tk.Frame(self.window)
        #tframe.pack()
        self.tframe.place(x=530, y=50)

        if self.tableIsEmpty():
            #print("Table is empty")
            self.table = TableCanvas(self.tframe, read_only=True)
            self.table.show()
        else:
            self.show_Data_in_table()

        #for top most label
        self.lbl = tk.Label(self.window, text='Enter Student details here:', width=30, height=2, fg='black', bg='gray', font=('times',20,'bold'))
        self.lbl.place(x=30,y=0)

        #for id field
        self.id_lbl = tk.Label(self.window, text='Enter ID:', width=10, height=2,fg='black', bg='pink', font=('times',15,'bold'))
        self.id_lbl.place(x=10,y=100)
        self.id_entry = tk.Entry(self.window, width=20, bg='white', fg='black', font=('times',25,'bold'))
        self.id_entry.place(x=150, y=100)
        #for id field

        #for name field
        self.name_lbl = tk.Label(self.window, text='Enter Name:', width=10, height=2,fg='black', bg='pink', font=('times',15,'bold'))
        self.name_lbl.place(x=10,y=160)
        self.name_entry = tk.Entry(self.window, width=20, bg='white', fg='black', font=('times',25,'bold'))
        self.name_entry.place(x=150, y=160)
        #for name field

        #for department field
        self.dept_lbl = tk.Label(self.window, text='Enter Dept.:', width=10, height=2,fg='black', bg='pink', font=('times',15,'bold'))
        self.dept_lbl.place(x=10,y=220)

        self.tkinter_variable = tk.StringVar(self.window)
        self.tkinter_variable.set("CSE") # default value
        OPTIONS = ["CSE", "IT", "ECE"]
        self.dept_entry = tk.OptionMenu(self.window, self.tkinter_variable, *OPTIONS)   #to get the selected value use - variable.get()
        self.dept_entry.configure(height = 2, width = 30)
        self.dept_entry.place(x=150, y=220)
        #for department field

        #for address field
        self.addr_lbl = tk.Label(self.window, text='Enter Address:', width=10, height=2,fg='black', bg='pink', font=('times',15,'bold'))
        self.addr_lbl.place(x=10,y=280)
        self.addr_entry = tk.Entry(self.window, width=20, bg='white', fg='black', font=('times',25,'bold'))
        self.addr_entry.place(x=150, y=280)
        #for address field

        #FOR Take image sample & Save BUTTON
        self.saveButton = tk.Button(self.window, text='Take image sample & Save', command=self.Take_image_sample_and_Save, fg='black', bg='white', width=20, height=1, activebackground='red', font=('times',20,'bold'))
        self.saveButton.place(x=60,y=450)
        #FOR Take image sample & Save BUTTON






















































'''
#FOR Update BUTTON
updateButton = tk.Button(window, text='Update', command='', fg='black', bg='white', width=8, height=1, activebackground='red', font=('times',20,'bold'))
updateButton.place(x=10,y=380)
#FOR Update BUTTON

#FOR Delete BUTTON
deleteButton = tk.Button(window, text='Delete', command='', fg='black', bg='white', width=8, height=1, activebackground='red', font=('times',20,'bold'))
deleteButton.place(x=170,y=380)
#FOR Delete BUTTON

#FOR Clear BUTTON
clearButton = tk.Button(window, text='Clear', command='', fg='black', bg='white', width=8, height=1, activebackground='red', font=('times',20,'bold'))
clearButton.place(x=330,y=380)
#FOR Clear BUTTON
'''



'''
#FOR Edit image sample & Data BUTTON
editButton = tk.Button(window, text='Edit image sample & Data', command='', fg='black', bg='white', width=20, height=1, activebackground='red', font=('times',20,'bold'))
editButton.place(x=60,y=530)
#FOR Take image sample & Save BUTTON
'''




