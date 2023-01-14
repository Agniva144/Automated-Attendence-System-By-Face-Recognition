import cv2
import numpy as np
import face_recognition
import csv
import os
from datetime import datetime

from PIL import ImageGrab
def funcRun():
    path = 'Training_images'
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
            encodeList.append(encode)
        return encodeList




    #### FOR CAPTURING SCREEN RATHER THAN WEBCAM
    # def captureScreen(bbox=(300,300,690+300,530+300)):
    #     capScr = np.array(ImageGrab.grab(bbox))
    #     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    #     return capScr

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)




    ##
    now=datetime.now()
    current_date=now.strftime("%Y-%m-%d")
    file_date=current_date+'.csv'
    # lnwriter=csv.writer(f)  #Instance of csv file 
    ##

    nameList=[]
    # if len(nameList)==0:


    # #Creating New file if not exist
    # if os.stat(file_date).st_size == 0:
    #     # print('File is empty')
    #     f=open(file_date,'w+',newline='') # One csv for one date
    #     lnwriter=csv.writer(f)  #Instance of csv file 
    #     lnwriter.writerow(['Name','Time'])


    # else:
    #     f=open(file_date,'a+',newline='') # One csv for one date
    #     lnwriter=csv.writer(f)  #Instance of csv file 
    #     # print('File is not empty')

    #Re-written code
    f=open(file_date,'w+',newline='') # One csv for one date
    lnwriter=csv.writer(f)  #Instance of csv file 
    lnwriter.writerow(['Name','Time'])






    while True:
        success, img = cap.read()
    # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()

                if name not in nameList:

                    current_time=now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])

                
                    print(name)
                    
                    nameList.append(name)

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Attendence System",img)

        key=cv2.waitKey(1)   #pauses execution of code(Press any key)--> assigning to wait for 1 sec
        if key==81 or key==113:
            break

    cap.release()
    cv2.destroyAllWindows()
    f.close    

funcRun()

# import pickle
# pickle.dump(funcRun(),'abc.pickle','wb')





#########################




# from flask import Flask, render_template, Response
# import cv2

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# def gen():
#     face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

#         ret, jpeg = cv2.imencode('.jpg', frame)
#         if ret:
#             yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == '__main__':
#     app.run()
