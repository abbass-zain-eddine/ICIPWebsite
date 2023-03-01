<h1>ICIP Competition applicaiton</h1>

this project creates a Docker container for an Flask application that is responsible for object detection in images. The application uses yolov8 trained on noisy COCO dataset. the dataset is provided by ICIP Conference Competition 2023. 
the project is designed as follow:
<ol>
<li><b>Static Folder:</b> This folder includes only one single folder called results and it is used to save the image with bounding boxes.</li>
<li><b>templates:</b> This folder include the home html page where the user is able to upload his image to be used by the model.</li>
<li><b>uploads:</b> Is the file where the uploaded images are saved.</li>
<li><b>yolov8: </b>I the folder where the ONNX weights of the trained model are saved.</li>
<li><b>app.py:</b> Is the main applicaiton file that loads the model and run the it on the uploaded image.</li>
<li><b>Dockerfile:</b>Is the known docer file to containarize the application.</li>
<li><b>Procfile:</b> is used by Heroku cloud to deploy the application.</li>
<li><b>requirements:</b> is the requirements file containing the necessary libraries to be installed.</li>
<li><b>runtime.txt:</b> It is to specify the python version to be used by Heroku cloud.</li>
<li><b>.github:</b> This folder contains one folder called workflows with one yaml file. the main.yaml file maintain the secure connection between github and Heroku</li>
</ol>
