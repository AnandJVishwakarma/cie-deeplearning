# -*- coding: utf-8 -*-

# from __future__ import division, print_function
# # coding=utf-8
# import sys
import os
import cv2
import numpy as np
import numpy as np
from PIL import Image
import psycopg2
import psycopg2.extras
from psycopg2 import Error
import tensorflow as tf
from keras.models import load_model
# Flask utils
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

'''Connect to PostgreSQL Database'''
DB_HOST = "localhost"
DB_NAME = "cyclone_intensity"
DB_USER = "postgres"
DB_PASSWORD = "root"

try:
    # establish connection with db
    connection = psycopg2.connect(user=DB_USER,
                                  password=DB_PASSWORD,
                                  host=DB_HOST,
                                  database=DB_NAME)

    connection.autocommit = True
    # create cursor to perform database operations
    cursor = connection.cursor()
    # print PostgreSQL details
    print("PostgreSQL server information:")
    print(connection.get_dsn_parameters(), "\n")
    # permanently commit changes to table
    # connection.commit()
except(Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)





#from gevent.pywsgi import WSGIServer
UPLOAD_FOLDER = 'static/uploads/'
UPLOAD_FOLDER1 = 'static/localized_img/'
# Define a flask app
app = Flask(__name__)
app.secret_key = 'super riri key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# # Model saved with Keras model.save()
model_path ='Ensemble_model1.h5'

model = load_model(model_path)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def localize(path):
    # Load the image
    img = cv2.imread(path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # Calculate the histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    import matplotlib.pyplot as plt

    # Display the histogram
    plt.hist(gray.ravel(), 256, [0, 256])
    ##plt.show()


    # Threshold the grayscale image
    ##ret, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Apply thresholding to create a binary image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)


    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Set the minimum width and height for the bounding rectangles
    min_width, min_height = 50, 50

    # Iterate through the contours and draw a bounding rectangle around each one
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        text = 'CYLONE DETECTED'
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
##        color = 2**16-1  # 65535 is white color for 16 bis image
        cv2.putText(img, text, (9,40), font, font_scale,(0,255,255), thickness)
        
        
        if w > min_width and h > min_height:        # Draw the bounding rectangle on the image
            cv2.rectangle(img, (x, y), ((x+ w), y + h), (0,0,0,), 3)
            break

    # Show the image with the bounding rectangles
    # cv2.imshow('Image with Bounding Rectangles', img)
    return img
  

# Model predicition
def model_predict(img_path, model):

    img = tf.keras.utils.load_img(img_path, target_size=(512,512))

    # Preprocessing the image
    x = tf.keras.utils.img_to_array(img)
    
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    # plt.imshow(x)
    x = np.expand_dims(x, axis=0)
   
    category = ""
# Be careful how your trained model deals with the input
# otherwise, it won't make correct prediction!
   # x = preprocess_input(x)
    preds = model.predict(x).round() #model.predict(x)

    if preds.round()< 17:
      category = "Extreme Low Cyclone"
    elif  17 <=  preds.round() <= 27:
      category = "Depression"
    elif 28 <=  preds.round() <= 33:
      category = "Deep Depression"
    elif 34 <=  preds.round() <= 47:
      category = "cyclonic storm"
    elif 48 <=  preds.round() <= 63:
      category = "Severe cyclonic storm"
    elif 64 <=  preds.round() <= 89:
      category = "Very Severe cyclonic storm"
    elif 90 <=  preds.round() <= 119:
      category = "Extreamely Severe cyclonic storm"
    elif preds.round()>= 120:
      category = "Super cyclonic storm"
    return {"preds":preds,'category': category}

# model = tf.keras.models.load_model('/content/drive/MyDrive/Cyclone/Ensemble_model.h5')
# model_predict('/content/drive/MyDrive/Cyclone/insat3d_ir_cyclone_ds/CYCLONE_DATASET_INFRARED/valid/106.jpg',model)

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/cal-intensity', methods=['GET','POST'])
def cie():
     return render_template('cie.html')


@app.route('/predict', methods=['POST'])
def upload_image():
    # get values from html form
    img_date = request.form.get("image_date")
    img_time = request.form.get("image_time")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
        
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      flash('No image selected for uploading')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      
      # # Save the file to ./uploads
      #main Iamge
      file_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
      file.save(file_path)
      #localized image
      im_rgb = cv2.cvtColor(localize(file_path), cv2.COLOR_BGR2RGB)
      Image.fromarray(im_rgb).save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))

    #   # Make prediction
      preds1 = model_predict(file_path, model) 
      print(preds1)


      # execute SQL Queries
      cursor.execute("""
                          INSERT INTO insat3d_data(upload_datetime, coordinates, intensity, cyclone_cat, images, img_date, img_time)
                          VALUES(current_timestamp,point(%s,%s), %s, %s, %s, %s,%s);""",
                      (latitude, longitude, str(int(preds1['preds'])), str(preds1['category']),filename, img_date, img_time))

      # # fetch result

      # record = cursor.fetchmany()
      # print(record, "\n")
      # close connection and commit to database
      connection.commit()

      print('upload_image filename: ', filename)
      print('image date: ', img_date)
      print('image time: ', img_time)
      print('cyclone latitude: ', latitude)
      print('cyclone longitude: ', longitude)


    #   flash('Image successfully uploaded and displayed below')
      return render_template('predict.html', filename=filename,filename_localized=os.path.join(app.config['UPLOAD_FOLDER1'], filename),
                             pred = preds1['preds'][0][0], category = preds1['category'])
    else:
      flash('Allowed image types are -> png, jpg, jpeg, gif')
      return redirect(request.url)
    
  
@app.route('/predict/<filename>')
def display_localizedimage(filename):
    
    # print('display_image flename: ' + filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)
    return render_template('predict.html', filename=filename,filename_localized=os.path.join(app.config['UPLOAD_FOLDER1'], filename))

@app.route('/<filename>')
def display_image(filename):
    # print('display_image flename: ' + filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)
    return render_template('image.html', filename=filename)

@app.route('/live-map')
def wind():
    # print('display_image flename: ' + filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)
    return render_template('windy.html')


# archive page
@app.route('/archive')
def archive():
    # execute SQL Queries
    cursor.execute("""
                SELECT * FROM insat3d_data
                ORDER BY upload_datetime DESC
                LIMIT 20;
                """)
    # # fetch result
    records = cursor.fetchall()
    print("Number of rows: ", len(records))

    arranged_records = []
    for row in records:
        # extract lat, long from coordinates(x,y) 
        separator = row[1].find(",")
        lat = row[1][1:separator]
        long = row[1][separator + 1:-1]

        predicted_intensity = row[4]
        cyclone_category = row[2]
        image_filename = row[3]
        capture_date = row[5].strftime("%d/%m/%Y")
        capture_time = row[6].strftime("%H:%M:%S")
        # print(lat, long, capture_date, capture_time, image_filename, predicted_intensity)

        record = dict(lat=lat, long=long, predicted_intensity=predicted_intensity,cyclone_category=cyclone_category,
                      image_filename=image_filename, capture_date=capture_date, capture_time=capture_time)
        arranged_records.append(record)
        # table_items = {lat, long, predicted_intensity, image_filename, capture_date, capture_time}

    # record = cursor.fetchmany()
    # print(record, "\n")
    # close connection and commit to database
    connection.commit()

    return render_template('archive.html', items=arranged_records)

@app.route('/about')
def about():
    # print('display_image flename: ' + filename)
    # return redirect(url_for('static', filename='uploads/' + filename), code=301)
    return render_template('newpage.html')

if __name__ == '__main__':
    app.run(port =6001, debug=True)
    
