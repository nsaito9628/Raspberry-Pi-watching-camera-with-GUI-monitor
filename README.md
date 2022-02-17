# Raspberry-Pi-watching-camera-with-GUI-monitor
It is a Raspberry Pi camera recorder that can make various settings on the GUI screen where you can select event recording or continuous recording.

<br>

## **Overview**
Event recording is trimmed 15 seconds before and after object detection by the camera, combined and saved. You can set the sensitivity for object detection.　　

For continuous recording, you can specify the start time and total recording time.　　

After mp4 conversion, the recorded video data will be uploaded to the preset Amazon S3 bucket.　　

<br>

## **GUI screen and setup steps**
<img src="img/picam_gui.gif">
<br />
<br />


## **Physical specifications**

#### **RaspberryPi**
Hardware: BCM2835  
Model: Raspberry Pi 4 Model B Rev 1.2  
microSD card: 32GB or more  

#### **4 inchi monitor**
https://www.amazon.co.jp/gp/product/B0896SXPXG/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1  

#### **USB camera**
logicool C270N  
<br>
<br />

## **Development environment**
#### **RaspberryPi**
Kernel: Linux    
Kernel release No.: 5.10.92-v7l+   
Kernel version: #1514 SMP Mon Jan 17 17:38:03 GMT 2022 armv7l    
OS： Raspbian GNU/Linux 11 (bullseye)  
Language: python 3.9.2  
<br/>

## **Construction procedure**

### **Preparation**
1. Prepare RaspberryPi OS image disc.  https://www.raspberrypi.com/software/
2. Insert the OS image disc into the Raspberry Pi and turn on the power.
3. Make initial settings for Raspberry Pi, ssh/VNC available and connect to the Internet.  
4. Connect c270n to USB 2.0 port.  
<br>

### **Building an environment on Raspberry Pi**
Start Raspberry so that it can connect to VNC and connect to the Internet.  
  
  
Clone this project from public repository
```sh  
git clone https://github.com/nsaito9628/Raspberry-Pi-watching-camera-with-GUI-monitor.git
```
  
Deploy a project  
``` sh
cp ./Raspberry-Pi-watching-camera-with-GUI-monitor/src/* ~
cp ./Raspberry-Pi-watching-camera-with-GUI-monitor/env/* ~
```

Download and unpack the required packages
```sh
sudo chmod u+x environment.sh
./environment.sh
```
  
Set aws configuration as default profile  
```sh
aws configure (Replace with your own key)  
    AWS Access Key ID[]: your Access Key ID
    AWS Secret Access Key []: your Secret Access Key
    Default region name []: ap-northeast-1
    Default output format []:
```

Customize parameters (if needed)  
``` sh
sudo nano env_const_config
```
Parameters customizable as below 
>CAM_NO  
S3BUCKET  
  
Registration of RaspberryPi as a thing to AWS IoT core and automatic startup setting
```sh
sudo chmod u+x env_const_prov.sh
./env_const_prov.sh
```

Restart Raspberry Pi and start recording
```sh
sudo reboot   
```
You can see it in the gif at the beginning of the README.md.  
After recording, recorded files can be downloaded from S3
<br>