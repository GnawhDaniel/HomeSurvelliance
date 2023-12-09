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


*Note: Other camera iterations can be used. But the code in this repository uses the picamera 2 library.*

## Installation (PC)
Under construction

## Usage
Under construction

## License

[MIT](https://choosealicense.com/licenses/mit/)