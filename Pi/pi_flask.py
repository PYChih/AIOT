from flask import Flask, request
from flask import send_file
from datetime import datetime
import requests
import os
import glob
import json

predict_list=[]

app = Flask(__name__)

@app.route('/postLabel', methods=['POST'])
def postLabel():
    content = request.json
    predict_list.append(str(content))
    print ("postLabel execute", datetime.now(), content)
    return "ok"
    
@app.route('/list', methods=['GET'])
def lists():
    print ("list:", json.dumps(predict_list))
    return json.dumps(predict_list)

@app.route('/clear', methods=['GET'])
def clear():
    print ("clear:")
    predict_list.clear()
    return "clear"
    
@app.route('/clearImg', methods=['GET'])
def clearImg():
    print ("clearImg:")
    files = glob.glob("/home/pi/final_project/img_folder/*.jpg")
    for f in files:
        print ("rm ",f)
        os.remove(f)
    return "clear"
    
@app.route("/img", methods=['GET'])
def img():
    filename = request.args.get("file")
    print ("filename:", filename)
    return send_file(filename, mimetype='image/jpg')

if __name__ == '__main__':
    app.run(host="192.168.0.103", port = 5000,
       debug = False, threaded = True)