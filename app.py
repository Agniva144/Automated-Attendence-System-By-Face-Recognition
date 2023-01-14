import cv2
import numpy as np
import face_recognition #
import csv
import pandas as pd
import os
from flask import Flask, jsonify

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




    ### FOR CAPTURING SCREEN RATHER THAN WEBCAM
    # def captureScreen(bbox=(300,300,690+300,530+300)):
    #     capScr = np.array(ImageGrab.grab(bbox))
    #     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    #     return capScr

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)
    # cap = captureScreen()




    ##
    now=datetime.now()
    current_date=now.strftime("%Y-%m-%d")
    # file_date=current_date+'.csv'
    # file_date='Attendence'+'.csv'
    
    # lnwriter=csv.writer(f)  #Instance of csv file 
    ##

    nameList=[]
   
    #Checking and file creating if not exist

    try:
        pd.read_csv('static/Attendence.csv')

    except:
        print("Something else went wrong")
        f=open("static/Attendence.csv",'w+',newline='') # One csv for one date
        lnwriter=csv.writer(f)  #Instance of csv file 
        lnwriter.writerow(['Name','Date','Time'])

    f=open("static/Attendence.csv",'a+',newline='') # One csv for one date
    lnwriter=csv.writer(f)  #Instance of csv file 






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
                    lnwriter.writerow([name,current_date,current_time])

                
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

    return nameList    
# funcRun()


## main 

from flask import Flask, jsonify, request,render_template,redirect,url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Training_images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/')
def index():
    return render_template('index.html')
    # return ("Hello")


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/intro',methods=['GET','POST'])
def intro():
    return render_template('intro.html')

@app.route('/upload',methods=['GET','POST'])
def upload():
    return render_template('upload.html')

# def my_function():
#     return "Hello, World!"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadDone', methods=['POST'])
def uploadDone():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    try:
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return 'File uploaded successfully. <br> <img src='+url_for('static', filename='uploads/' + file.filename)+'/>'
            return render_template('intro.html',data="Successfully Uploaded !")
        else:
            return 'File not allowed!'
    # return render_template('intro.html',data="Successfully Uploaded !")
    except Exception as e:
        # code to handle the internal server error
        return jsonify(error=str(e)), 500




# @app.route('/run_function')
@app.route('/run_function', methods=['POST'])
def run_function():
    # return my_function()
    result=funcRun()
    # result = funcRun()
    # return jsonify(result)
    return redirect('/intro')
    # return result



if __name__ == '__main__':
    app.run()

##


####
# from flask import Flask, request, render_template, url_for
# import os

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


# # @app.route('/run_function')
# # def run_function():
# #     # result = my_function()
# #     # return jsonify(result)

# @app.route('/')
# def index():
# #     return render_template('index.html')
#     result = funcRun()
#     # return jsonify(result)


# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# # @app.route('/upload', methods=['POST'])
# # def upload():
# #     file = request.files['file']
# #     if file and allowed_file(file.filename):
# #         filename = file.filename
# #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# #         return 'File uploaded successfully. <br> <img src='+url_for('static', filename='uploads/' + file.filename)+'/>'
# #     else:
# #         return 'File not allowed'


# if __name__ == '__main__':
#     app.run()
