# Pheebs

A Visual Object Tracking Application with Frame to Frame Data Propagation.

## System requirements

- Python `V3.6` or later
- IP camera with `RTSP` stream

## Installation 

1. Download the project from GitHub
1. Install the required dependencies by running `~/$ pip3 install -r requirements.txt`
    > Make sure you are in the root directory of the project 
1. Open the `detect.py` file in a text editor of your preference
1. Find line `30` and replace the `RTSP` stream address with yours.
```python
30.  cap = VideoStream('rtsp://admin:admin1@10.10.240.43:554/11').start()
```
The RTSP address should have the following format: 
   
```text
rtsp://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:554/11
```

## Start Pheebs

After completing the installation, in a terminal window navigate to the root of the project and run:
```shell script
~/$ ./pheebs.sh
``` 
You should see a window with the feed from your camera and the following information in your terminal.
![](terminal.png)

## Centroid Tracking Algorithm
> The centroid tracking algorithm used in this project is based on  [Simple object tracking with OpenCV](https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/) by Adrian Rosebrock

## Project Presentation
The Project presentation is available on YouTube. [Watch now](https://www.youtube.com/watch?v=21ux48TsWIs)

## Dependencies

> All Dependencies can be found in ```requirements.txt```

```text
absl-py==0.9.0
astor==0.8.1
cachetools==4.1.0
certifi==2018.4.16
chardet==3.0.4
Click==7.0
cmake==3.17.2
cycler==0.10.0
dlib==19.19.0
Flask==0.12.2
gast==0.2.2
google-auth==1.14.1
google-auth-oauthlib==0.4.1
google-pasta==0.2.0
grpcio==1.28.1
h5py==2.10.0
idna==2.7
imutils==0.5.3
ItsDangerous==1.0.0
Jinja2==2.10
joblib==0.14.1
Keras==2.3.1
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.0
kiwisolver==1.2.0
Markdown==3.2.1
MarkupSafe==1.0
matplotlib==3.2.1
numpy==1.17.0
oauthlib==3.1.0
opencv-python==4.2.0.32
opencv-python-headless==4.2.0.32
opt-einsum==3.2.1
paho-mqtt==1.4.0
Pillow==7.1.2
protobuf==3.11.3
pyasn1==0.4.8
pyasn1-modules==0.2.8
pymessenger==0.0.7.0
pyparsing==2.4.7
python-dateutil==2.8.1
python-dotenv==0.9.1
PyYAML==5.3.1
requests==2.23.0
requests-oauthlib==1.3.0
requests-toolbelt==0.8.0
rsa==4.0
Rx==3.0.1
scikit-learn==0.22.1
scipy==1.4.1
six==1.14.0
sklearn==0.0
tensorboard==2.1.1
tensorflow==2.1.0
tensorflow-estimator==2.1.0
termcolor==1.1.0
urllib3==1.23
Werkzeug==0.14.1
wrapt==1.12.1
```



> Inspired in Mykonos.
