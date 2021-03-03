import cv2
import numpy as np 
import time
import requests
from datetime import date
from datetime import datetime

#today = date.today()
#print("Today's date:", today)
base_dir = "/home/pi/final_project/face_network/tiny_fddb_0301_long"

def load_yolo():
	net = cv2.dnn.readNet(base_dir + "/backup/tinyv3_fddb_last.weights", base_dir + "/tinyv3_fddb.cfg")
	# net = cv2.dnn.readNet(base_dir + "yolov3-tiny.weights", base_dir + "yolov3-tiny.cfg")
	classes = []
	with open(base_dir + "/tinyv3_fddb.names", "r") as f:
		classes = [line.strip() for line in f.readlines()]

	layers_names = net.getLayerNames()
	output_layers = [layers_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
	colors = np.random.uniform(0, 255, size=(100, 3))
	return net, classes, colors, output_layers

def start_webcam():
	cap = cv2.VideoCapture(0)
	return cap

def detect_objects(img, net, outputLayers):			
	blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(192, 192), mean=(0, 0, 0), swapRB=True, crop=False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return blob, outputs

def get_box_dimensions(outputs, height, width):
	boxes = []
	confs = []
	class_ids = []
	for output in outputs:
		for detect in output:
			scores = detect[5:]
			class_id = np.argmax(scores)
			conf = scores[class_id]
			
			if conf > 0.5:
#				print ("detect:",detect)
				center_x = int(detect[0] * width)
				center_y = int(detect[1] * height)
				
				w = int(detect[2] * width)
				h = int(detect[3] * height)
				x = int(center_x - w / 2)
				y = int(center_y - h / 2)
				boxes.append([x, y, w, h])
				confs.append(float(conf))
				class_ids.append(class_id)
				
#				print ("scores:",scores, "class_id:",class_id, "conf:", conf, "center_x:", center_x, "center_y:", center_y, "w:",w,"h:",h,"x:",x,"y:",y)
	return boxes, confs, class_ids

def draw_labels(boxes, confs, colors, class_ids, classes, img): 
	indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.0)
#	print ("indexes: ",indexes)
	font = cv2.FONT_HERSHEY_PLAIN
	for i in range(len(boxes)):
#		print ("i:",i,"draw_labels:\t",i)
		if True:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			conf = confs[i]
			color = colors[i%3]

			cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
			cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
			today = date.today()
			now = datetime.now()
			imgFileName = "img_folder/" + str(now).replace(":","_").replace(" ","_")+"_"+label+".jpg"
			r = requests.post('http://192.168.0.103:5000/postLabel', json={"label":label,"x":x,"y":y,"w":w, "h":h, "img":imgFileName})
			print("conf: {:.2f}, label {}".format(conf, label))
			#print("now:", now, "conf:", conf, "label:", label, "x:",x, "y:",y, "w:",w, "h:",h, "img:", imgFileName)
			cv2.imwrite(imgFileName, img)
	cv2.imshow("test", img)

def webcam_detect():
	model, classes, colors, output_layers = load_yolo()
	cap = start_webcam()
	
	while True:
		_, frame = cap.read()
		height, width, channels = frame.shape
		blob, outputs = detect_objects(frame, model, output_layers)
		boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
		draw_labels(boxes, confs, colors, class_ids, classes, frame)
		key = cv2.waitKey(1)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()

if __name__ == '__main__':
	webcam_detect()
	cv2.destroyAllWindows()