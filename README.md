# IOT Project - Security Camera

Welcome to my IoT project, an application developed as part of an undergraduate computer science course. This project integrates a Raspberry Pi with a Python-based server through websockets, creating a broadcast from the camera from the Raspberry Pi.

One of the standout features of this project is the use of YOLO (You Only Look Once) algorithm for real-time people classification. YOLO allows the system to intelligently identify and classify people in the video frame in real time.

Utilizing websockets, the system enables the Raspberry Pi to transmit a stream of images to a server operating on a local computer. Once these images are received, the server employs the YOLO algorithm to determine the presence of a person within each image. In cases where a person is detected, the algorithm delineates the individual by drawing a bounding box around them.

The primary goal of this project is to demonstrate the effective application of websockets in real-time data transmission, highlighting how a compact and cost-effective device like the Raspberry Pi can be transformed into a potent broadcasting tool equipped with advanced machine learning capabilities. The project serves as an invaluable learning experience in several domains, including networking, hardware integration, web development, and AI.

## Hardware Required
1. Raspberry Pi Zero 2W
2. Raspberry Pi Camera V2 (Noir) 

## PC Specs during Project
- CPU: Intel i5-10600k
- GPU: RTX 2070 Super
- RAM: 32 GB


*Note: Other camera modules can be used. But the code in this repository uses the picamera 2 library.*

## Installation
To install and run, follow these steps:

1. **Clone the Repository**
    - Open your terminal.
    - Clone the repository using Git:
      ```
      git clone git@github.com:GnawhDaniel/Home-Security-Camera.git
      ```
    - Navigate to the cloned directory:
      ```
      cd Home-Security-Camera
      ```
2. **Setting up Prerequisites**
    - Install [Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html).
    - Create new conda environment.
      ```
      conda create -n [env-name] python=3.11.5
      conda activate [env-name]
      ```
    - Install [PyTorch](https://pytorch.org/get-started/locally/).
    - Install necessary libraries.
      ```
      conda install -c conda-forge ultralytics websockets python-dotenv
      ```
    - Install necessary packages for launching the website.
      ```
      cd website
      npm i
      ```

3. **Raspberry Pi Set-up**
    - Insert Camera Module into CSI slot.
    - Flash Raspberry Pi OS to Raspberry Pi using the [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
    - SSH into the RPI terminal and update software.
      ```
      sudo apt update && sudo apt upgrade
      ```
    - Install websockets library.
      ```
      sudo apt install python3-websockets
      ```
    - Then create a new python file and copy the [Raspberry Pi Code](https://github.com/GnawhDaniel/Home-Security-Camera/blob/main/raspberrypi/main.py) into the file.

4. **Obtaining IP Address and Setting Up Endpoints**
    - Run server.py script.
      ```
      cd server
      python server.py
      ```
    - Copy the address printed in the terminal (ws://[IP-Address]:5000).
    - Navigate to .env file in website/.env and replace the value in VITE_SERVER_URL with the copied ip address.
    - Then on the Raspberry Pi manually replace the IP_ADDRESS variable with the copied address as well.

5. **Setting Up Gmail App Credentials**
    - Please do not share Google App password with anyone!
    - Navigate to the [Google's App Setup Guide](https://support.google.com/mail/answer/185833?hl=en) and follow the instructions.
    - In the .env file in the server directory, write the application email and password into their respective fields.

7. **Running the System**
    - Ensure server.py script is running.
    - Navigate the to website directory, and type `npm run dev` to launch website.
    - Run python script on the Raspberry Pi via SSH terminal using `python3 main.py`
    - The live stream from the Raspberry Pi camera should now be viewable on the website.
