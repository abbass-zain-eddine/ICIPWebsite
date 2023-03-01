from flask import Flask,request,render_template
import numpy as np
import onnxruntime
import os,cv2
from cv2 import imread



app=Flask(__name__)

# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = "./uploads"
model_path="./yolov8/best.onnx"
weights_path="./yolov8/best.pt"
configuration_path="./yolov8/yolov8m.pt"
model=onnxruntime.InferenceSession(model_path,None)
#model=YOLO(weights_path)
CLASSES=['person','bicycle','car','motorcycle','airplane','bus','train','truck','boat','traffic light','fire hydrant','street sign'\
         ,'stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','hat',
'backpack','umbrella','shoe','eye glasses','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite'\
    ,'baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','plate','wine glass','cup','fork','knife'\
        ,'spoon','bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','couch'\
            ,'potted plant','bed','mirror','dining table','window','desk','toilet','door','tv','laptop','mouse','remote','keyboard'\
                ,'cell phone','microwave','oven','toaster','sink','refrigerator','blender','book','clock''vase','scissors','teddy bear'\
                    ,'hair drier','toothbrush','hair brush']
colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))
# Define secret key to enable session
app.secret_key = 'THISMYKEY'
 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
    image_name=""
    if request.files or 'image' in request.files: 
        uploaded_img=request.files['image']
        image_name= uploaded_img.filename
        image_saved_path=os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        uploaded_img.save(image_saved_path)
        model: cv2.dnn.Net = cv2.dnn.readNetFromONNX('./yolov8/best.onnx')
        original_image: np.ndarray = cv2.imread( image_saved_path)
        [height, width, _] = original_image.shape
        length = max((height, width))
        image = np.zeros((length, length, 3), np.uint8)
        image[0:height, 0:width] = original_image
        scale = length / 640

        blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255, size=(640, 640))
        model.setInput(blob)
        outputs = model.forward()

        outputs = np.array([cv2.transpose(outputs[0])])
        rows = outputs.shape[1]

        boxes = []
        scores = []
        class_ids = []

        for i in range(rows):
            classes_scores = outputs[0][i][4:]
            (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
            if maxScore >= 0.25:
                box = [
                    outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                    outputs[0][i][2], outputs[0][i][3]]
                boxes.append(box)
                scores.append(maxScore)
                class_ids.append(maxClassIndex)

        result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)

        detections = []
        for i in range(len(result_boxes)):
            index = result_boxes[i]
            box = boxes[index]
            detection = {
                'class_id': class_ids[index],
                'class_name': CLASSES[class_ids[index]],
                'confidence': scores[index],
                'box': box,
                'scale': scale}
            detections.append(detection)
            draw_bounding_box(original_image, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                            round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))

        cv2.imwrite("./static/results/" + image_name, original_image)

    return render_template("home.html",model_output="./static/results/"+image_name)


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f'{CLASSES[class_id-1]} ({confidence:.2f})'
    color = colors[class_id]
    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)
    cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


if __name__=="__main__":
    
    app.run(debug=False)
