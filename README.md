# cie-deeplearning
## Cyclone Intensity Estimation using Deep Learning

A Deep learning web app to estimate cyclone intensity estimation using INSAT-3D satellite data as there is need of automated and reliable method.
The  user can upload INSAT-3D IR Satellite Image of Cyclone which is then passed to our Deep Convolutional Neural Network ensembel model which is trained on Cyclone imagery of various intensities on the dataset from  Raw INSAT-3D satellite captured images on MOSDAC server.


 The user can also enter metadata values like date time and latitudinal position for the cyclonic event, which will be stored in a database and used to build an archive of past cyclonic events. Users can view the past events and associated metadata in the archive and visualize the localized imagery. The Flask web framework is used to integrate the web application in Python. Overall, this application uses image processing, deep learning, and database integration to provide users with accurate and timely information about cyclonic events.


## Dataset 
[Dataset link](https://www.kaggle.com/datasets/sshubam/insat3d-infrared-raw-cyclone-images-20132021)

## Technology Used

## Tech Stack Used

Front-end: HTML , CSS, Bootstrap and JavaScript

Back-end: PostgreSQL, Flask, psycopg2 and Python

Deep-learning-pipeline: Tensorlfow

Model used : [1] Mobilenet V2
[2] VGG16
[3] Inception
[4] Xception

``Home section:`` First  Page of the website

<<<<<<< HEAD
![Home](https://github.com/Rehan-99/cie-deeplearning/assets/54002059/91d4fe40-728a-4bfd-a7ca-db482daa6564)
=======
![Home](https://github.com/Rehan-99/cie-deeplearning/assets/54002059/91d4fe40-728a-4bfd-a7ca-db482daa6564))
>>>>>>> 5306f5a (updating readme)


``Form section:`` used to pass the image to the model which computes intensity and forwards input data to the  database.

![predict](https://github.com/Rehan-99/cie-deeplearning/assets/54002059/b0917d7a-d6c5-495b-b0f4-4624ca3bf40c)

``Live Weather Map:`` made using Windy API, showing live wind patterns and redirects the map to the coordinates recieved as input, incase of a cyclone, highlights the area with strong wind pattern.

![windy](https://github.com/Rehan-99/cie-deeplearning/assets/54002059/a1bed201-4df7-464e-a5f5-7d2bf8b218f7)


``Archive Table:`` Displaying all previously uploaded data which stored in database
![database](https://github.com/Rehan-99/cie-deeplearning/assets/54002059/59f6a49c-07ef-441f-8802-0e4da1321cdf)


``Submitted Image:`` Input Image willbe dispalyed as Localized Image along with intensity and Category of Cyclone
![output](https://github.com/Rehan-99/cie-deeplearning/assets/54002059/8880b5cb-5414-466c-beb8-88388cfa976f)


