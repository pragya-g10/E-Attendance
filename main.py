import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk




root = tk.Tk()
root.geometry("1200x1000")
cur_date=datetime.today()
root.title("CU_Hazir_Hain...")






path = 'C:\\Users\\Siddhant Tiwari\\PycharmProjects\\E_attendance-Project\\images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList. append(encode)
    return encodeList


def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()


        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M')
            f.writelines(f'\n{name},{dtString}')
            return  dtString
    return "Already Marked"

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(cv2.CAP_DSHOW)

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()


            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255,0), 6)
            cv2.rectangle(img, (x1, y2 - 25), (x2, y2), (0, 255,0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 4)
            entry_time = markAttendance(name)

            str_path = 'C:\\Users\\Siddhant Tiwari\\PycharmProjects\\E_attendance-Project\\images\\'
            str_path1 = myList[matchIndex]
            t_path = str_path + str_path1
            print(t_path)
            
            photo = tk.PhotoImage(file = t_path)

            tk.Label(root, text="Chandigarh University Attendance System ", fg="black", font="Arial 20 bold").grid(
                row=0, column=0)
            tk.Label(root, text="Student Details", fg="black", font="Broadway 20 bold").grid(row=2, column=5)
            f1 = tk.Frame(relief="raised", padx=10, pady=20).grid(row=1, column=0)
            f2 = tk.Frame(relief="raised", padx=10, pady=10).grid(row=4, column=4, rowspan=4)
            tk.Label(f1, image=photo).grid()
            

            tk.Label(f2, text="NAME : ", fg="black", font="Arial 16 bold").grid(row=4, column=5)
            tk.Label(f2, text=name, fg="black", font="Arial 16 bold").grid(row=4, column=6)
            tk.Label(f2, text="Department :", fg="black", font="Arial 16 bold").grid(row=5, column=5)
            tk.Label(f2, text="CSE", fg="black", font="Arial 16 bold").grid(row=5, column=6)
            tk.Label(f2, text="Entry time :", fg="black", font="Arial 16 bold").grid(row=6, column=5)
            tk.Label(f2, text=entry_time, fg="black", font="Arial 16 bold").grid(row=6, column=6)
            tk.Label(f2, text="Date :", fg="black", font="Arial 16 bold").grid(row=7, column=5)
            tk.Label(f2, text=str(cur_date), fg="black", font="Arial 16 bold").grid(row=7, column=6)

            tk.Label(root, text="Attendance Done", fg="black", font="Broadway 18 bold").grid(row=8, column=6)
            root.mainloop()



    cv2.imshow('Webcam', img)
    cv2.waitKey(1)