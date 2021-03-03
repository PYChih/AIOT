from flask import Flask, request
from pymongo import MongoClient
import requests

app = Flask(__name__, static_url_path='/static')

# connect to mongo server
client = MongoClient(host = '127.0.0.1', port = 8080)
db = client['yolo_pred_db'] # database name
coll = db['test_coll'] # collection

@app.route('/', methods=['GET'])
def list():
    htmlContent="<html>"
    htmlContent=htmlContent+"<head><meta http-equiv='refresh' content='10'></head>"
    htmlContent=htmlContent+"<table border=1 cellspacing=0 cellpadding=5>"
    htmlContent=htmlContent+"<tr><th>label</th><th>x</th><th>y</th>"
    htmlContent=htmlContent+"<th>w</th><th>h</th><th>filename</th><th>img</th></tr>"

    mydoc = coll.find().sort("img",-1).limit(10)
    count=1
    for i in mydoc:
        x="<tr>"
        x=x+"<td>"+str(count)+"</td>"
        x=x+"<td>"+i['label']+"</td>"
        x=x+"<td>"+str(i['x'])+"</td>"
        x=x+"<td>"+str(i['y'])+"</td>"
        x=x+"<td>"+str(i['w'])+"</td>"
        x=x+"<td>"+str(i['h'])+"</td>"
        x=x+"<td>"+'static/'+i['img']+"</td>"
        x=x+"<td><img width='128' src='/static/"+i['img']+"'></td>"
        htmlContent=htmlContent+x
        x=x+"</tr>"
        count=count+1
 
    htmlContent=htmlContent+"</table></html>"
    return htmlContent

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 3000,
       debug = False, threaded = True)