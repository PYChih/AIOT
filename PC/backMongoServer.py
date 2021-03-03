from pymongo import MongoClient
import requests
import base64
import datetime
import time
import json

def clear():
    clear_url = url+'/clear'
    r = requests.get(clear_url)
    if r.status_code == requests.codes.ok:
        print("clear_OK")

def getImg(j, filename):   # write inference image on pc
    img_url = url+'/img?file='+filename # this url can read img on pi
    with open('static/'+filename, 'wb') as handle:
        response = requests.get(img_url, stream=True)
        if not response.ok:
            print ("not response ok : "+ response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

    with open('static/'+filename, "rb") as f: 
        bin_pic = base64.b64encode(f.read()).decode('utf-8') # encode
        mydata = {'label':j['label'], 'x':j['x'], 'y':j['y'], 'w':j['w'], 'h':j['h'], 'img': filename, 'image_data': bin_pic}
        result = coll.insert_one(mydata) # save data to mongo

def fetchYoloResult():  # get inference dictionary
    datetime_dt = datetime.datetime.today()
    datetime_str = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")  # 格式化日期
    print ("fetchYoloResult:"+datetime_str)
    r = requests.get(url+'/list')
    if r.status_code == requests.codes.ok:
        print(r.text)

    # convert to json
    yolo_result = r.text
    yolo_json = json.loads(yolo_result)

    for j in yolo_json:
        detect_result = eval(j)
        img=detect_result['img'] # get img file name
        getImg(detect_result, img)
    clear()

url = 'http://192.168.0.103:5000' # pi flask web
client = MongoClient(host = '127.0.0.1', port = 8080)
db = client['yolo_pred_db']
coll = db['test_coll']

while True:
	fetchYoloResult()
	time.sleep(30)