from ultralytics import YOLO
from flask import Flask,request,app,jsonify,render_template,session
#import numpy as np
#import base64
from PIL import Image
#import io,os
import os
from DrawBoundingBoxes import BboxPlot
from cv2 import imread


app=Flask(__name__)

# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = "./uploads"
weights_path="./yolov8/best.pt"
configuration_path="./yolov8/yolov8m.pt"
model=YOLO(weights_path)
classes=['person','bicycle','car','motorcycle','airplane','bus','train','truck','boat','traffic light','fire hydrant','street sign'\
         ,'stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','hat',
'backpack','umbrella','shoe','eye glasses','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite'\
    ,'baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','plate','wine glass','cup','fork','knife'\
        ,'spoon','bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','couch'\
            ,'potted plant','bed','mirror','dining table','window','desk','toilet','door','tv','laptop','mouse','remote','keyboard'\
                ,'cell phone','microwave','oven','toaster','sink','refrigerator','blender','book','clock''vase','scissors','teddy bear'\
                    ,'hair drier','toothbrush','hair brush']
# Define secret key to enable session
app.secret_key = 'THISMYKEY'
 
@app.route('/')
def home():
    return render_template('home.html')


# @app.route('/predict_api',methods=['POST'])
# def predict_api():
#     data=request.json['image']
#     image_name=request.json['imgName']
#     base64_img=base64.b64decode(data.encode('utf-8'))
#     img=Image.open(io.BytesIO(base64_img))
#     img=np.asarray(img)
    
#     predicted = model.predict(img)
#     image_with_bboxes=BboxPlot(img,predicted[0].boxes.cpu().numpy()[:,[5,4,0,1,2,3]],classes).yolov8Plot(save_path="./results",img_name=image_name)
#     return jsonify(image_with_bboxes)


@app.route('/predict',methods=['POST'])
def predict():
    image_name=""
    if request.files or 'image' in request.files: 
        
        uploaded_img=request.files['image']
        image_name= uploaded_img.filename
        image_saved_path=os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        uploaded_img.save(image_saved_path)
        #session['uploaded_img_file_path']=os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        #base64_img=base64.b64decode(data.encode('utf-8'))
        #img=Image.open(io.BytesIO(base64_img))
        #img=np.asarray(img)
        
        img = imread(image_saved_path)
        predicted = model(img)
        BboxPlot(img,predicted[0].boxes.cpu().numpy()[:,[5,4,0,1,2,3]],classes).yolov8Plot(save_path="./static/results",img_name=image_name)
        session["path"]="./static/results/"+image_name
    return render_template("home.html",model_output="./static/results/"+image_name)



if __name__=="__main__":
    app.run(debug=True)
