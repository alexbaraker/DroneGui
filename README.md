## DroneGui

The GUI and networking portions of the Drone project work hand-in-hand to enable transfer of data from the drone to the local machine. The GUI application running on the local machine then visualizes the transferred data as well as processes visual information for the drone to respond to. The system for this is written in Python 3 and can be run on any Python 3 compatible environment including Windows, Linux, and Mac OS. A network capable of 2 Mbps data transfer is recommended for best performance.

## GUI Features

![](https://i.imgur.com/l4ER1uc.png)

The GUI is split up into 3 panels: Image viewer, Metrics & Controls, and Raw Value display. The image viewer allows to see a feed from the drone’s camera. If an orange ball is detected, the coordinates of the ball’s location in pixels is are updated in the top left corner. The Metrics &amp; Controls are meant for adjusting parameters that affect the detection of the ball, but have been deprecated following the perfection of the ball detection algorithm. Raw Value display features the PWM duty cycles for each of the 4 motors present on the drone for troubleshooting.


## Ball Detection

A dedicated class was created for image processing to partially isolate it from the rest of the code. This allows the work on the image processing be done independently without touching other files. The algorithm for detecting the ball is based off the work done by Adrian Rosebrock at [https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv](PyImageSearch). A general function, `detect_circles` in *image_processing.py*, was made to detect orange colored balls which is then called from `apply_image_changes` in gui.py. It operates on an openCV image with no additional data required. The process chain for detection is given by:

![](https://i.imgur.com/0nM559G.png)

The Gaussian Blur helps to remove any grain and artifacts that may otherwise cause difficulties for the blob filtering part of the detection. Converting to an HSV color format allows finer control over which color space is focused on. After masking for the desired color space, any artifacts and noise is filtered. Contour detection returns outlines of the remaining blobs. Finally, the largest contour becomes the centroid for which the minimum enclosing circle is then calculated. If there are no detections after this process the function returns a `(None, None)` detection point.

The pipeline for applying image frames and transmitting data is given by:

![](https://i.imgur.com/dM8OctP.png)

When `NetClient` receives the image frame data, the internal image data is refreshed and sent off for processing. After processing, the displayed image is updated and the detection data is sent off to the drone.

## Network Architecture

The network communication architecture of the drone system can be described using 3 nodes representing machines:

![](https://i.imgur.com/fEp5SbX.png)

Both the machine running the GUI and the machine running Simulink communicate over the network. While the Simulink side drives the motor controls of the drone, it can be thought as a black box from the perspective of the GUI side. All that is needed to be known is that this black box reads data stored in the drone’s memory and writes back to it. There are two pieces of data the Simulink side deals with that is needed for the GUI side: PWM duty cycles and pixel coordinates for ball tracking.

## Data Communications

![](https://i.imgur.com/CxsgSuJ.png)

The data communication models consists of two machines communicating with each other over a network. The drone has a server which interfaces with the system’s internal memory. The remote machines has a client which interfaces with the GUI launched along with it. Two types of network communications present, Control and Stream, allow to either control the drone or stream data.

Control type communication allows the client to request the server to carry out a function. After the function is executed, the server transmits back the function’s return to be acknowledged by the client.

![](https://i.imgur.com/kBdFtAE.png)
Model for control type communication

Stream type communication is a unidirectional data transfer method that allows the server to stream continuous data to the client:

![](https://i.imgur.com/yXdp5K7.png)
Model for stream type communication

The network system makes use of the ZMQ library to send data over the network. Since the ZMQ library does not track the connectivity of the server and client, this has to be done manually by having the client ping the server continuously. The connections are set up to be non-blocking, and because of this additional care needs to be taken in handling sudden disconnections between the client and server. This is done on the client side.

__CtrlServer & CtrlClient event faults:__

  _ | **Event description** | **Mitigating Behavior**
------------ | ------------- | -------------
**Normal Operation** | _ | Data is sent successfully and a reply is awaited with a timeout of 10 ms. Upon receiving a reply, data can be then be sent again successfully to which a reply is awaited for once again 
**Not able to respond in time** | Data is send and a reply is awaited with a timeout of 10 ms. The reply is not received within 10 ms and the receiver times out | The client does 10 attempts to receive the data to which the erver should respond to.
**Sudden Disconnect Event** | Data is sent and a reply is awaited with a timeout of 10 s. The reply is not received within 10 ms and the receiver times out. | The client does 10 attempts to receive the data to which the server does not respond to. The client will keep retrying to receive data with a timeout of 10 ms and 10 attempts until it eventually gets a response.
**Sudden restart event** | Data is send and a reply is awaited with a timeout of 10 ms. The reply is not received within 10 ms and the receiver times out. A reply will never be received because the server is awaiting for data to be sent. | The client will attempt to send data in addition to attempting to receive data.

Unlike the CtrlClient, StreamClient does not expect a reply from the server. As a result, it can wait for data until it receives it.

  _ | **Event description** | **Mitigating Behavior**
------------ | ------------- | -------------
**Normal Operation** | _ | StreamClient successfully receives data from StreamServer
**Sudden Disconnect Event** | No data is received by StreamClient | StreamClient awaits data from StreamServer
**Sudden restart event** | No data is received by StreamClient | StreamClient awaits data from StreamServer

## Clients &amp; Servers:

The data transmitted between every client and server consists of a topic and data. The topic is optional and is used to either indicate what the data being transmitted is or as a general indicator for the server to do something.

`uplink_server`:

**Type** | **Port** | **Rate** | **Notes**
-------- | -------- | --------- | ----------
CtrlServer | 5110 | 10 ms | Enables the client to know whether it is connected. A ‘ping’ is sent from the client every 10 ms to for the server to respond to. Failure to respond indicates connectivity issues with the server or data failed to process realtime.

**Topic** | **Request** | **Response** | **Notes**
-------- | -------- | --------- | ----------
N/A | ‘ping’ | ‘pong’ | 

`ctrl_server`:

**Type** | **Port** | **Rate** | **Notes**
-------- | -------- | --------- | ----------
CtrlServer | 5111 | aync | A server that enables controlling the drone remotely. Two implemented controls are the Killswitch and object tracking

**Topic** | **Request** | **Response** | **Notes**
-------- | -------- | --------- | ----------
‘KILLSWITCH’ | True | None | Triggers a kill switch routine that brings the drone down.
‘ROT’ | `([int]ball_x, [int]ball_y)` | None | This controls drone’s focus toward on a location as perceived in its camera feed by rotating to center the point in the camera’s visual space.

`pwm_status_server`:

**Type** | **Port** | **Rate** | **Notes**
-------- | -------- | --------- | ----------
StreamServer | 5112 | 10 ms | A server that streams PWM duty cycle data to the client

**Topic** | **Data** | **Notes**
-------- | -------- | ---------
‘PWM1’ | `[int]pwm_duty_cyle` | Sends PWM duty cycle data for motor1
‘PWM2’ | `[int]pwm_duty_cyle` | Sends PWM duty cycle data for motor2
‘PWM3’ | `[int]pwm_duty_cyle` | Sends PWM duty cycle data for motor3
‘PWM4’ | `[int]pwm_duty_cyle` | Sends PWM duty cycle data for motor4

`cam_stream`:

**Type** | **Port** | **Rate** | **Notes**
-------- | -------- | --------- | ----------
StreamServer | 5113 | 10 ms | A server streams camera frames to the client

**Topic** | **Data** | **Notes**
-------- | -------- | ---------
‘CAM’ | Binary data | Base64 encoded jpg image


## Memory Interface

The server interacts with the memory interface via `/dev/mem`.


**Name** | **Address** | **Size (bytes)** | **Notes**
-------- | -------- | --------- | ----------
ADDR_KILLSWITCH | 0x43C30000 | 4 | When first bit is high, triggers a kill switch routine that brings the drone down.
ADDR_PWM1 | 0x43C30000 + 4 | 4 | Contains the pwm duty cycles values of motor 1 on the drone. Acceptable values range from 50000 (off) to 70000 (full power).
ADDR_PWM2 | 0x43C40000 + 4 | 4 | Contains the pwm duty cycles values of motor 2 on the drone. Acceptable values range from 50000 (off) to 70000 (full power).
ADDR_PWM3 | 0x43C60000 + 4 | 4 | Contains the pwm duty cycles values of motor 3 on the drone. Acceptable values range from 50000 (off) to 70000 (full power).
ADDR_PWM4 | 0x43C70000 + 4 | 4 | Contains the pwm duty cycles values of motor 4 on the drone. Acceptable values range from 50000 (off) to 70000 (full power).
ADDR_LED | 0x43C80000 | 4 | Controls the LED present on the drone via first bit.
ADDR_CAM | 0xFFFC1000 | 8 | Has functionality dealing with object tracking. This controls drone’s focus toward on a location as perceived in its camera feed by rotating to center the point in the camera’s visual space. It is expected that the info fed to it is updated appropriately to reflect the drone’s response. Data consist of 4 bytes of data representing x-coordinate and 4 bytes representing y-coordinate, in px, respectively.


## Appendix I: Object Hierarchies

![](https://i.imgur.com/JwlW6ES.png)

**Figure 1:** The main initialization in run.py consists of instantiations of `NetClient` and `MainWindow`

&nbsp;

![](hhttps://i.imgur.com/y8vE1jS.png)

**Figure 2:** `NetClient` consists four instantiations of clients

&nbsp;

![](https://i.imgur.com/EuQiwKc.png)

**Figure 3:** `MainWindow` consists of three panels consisting of: `ImageViewerWidget` widget, the `Calibration` widget and the `MetricsDisplay` widget, respectively.


## Appendix II: Event Calls

![](https://i.imgur.com/zVR584j.png)

**Figure 4:** Each of pwm_client’s topics are hooked to their own callbacks which allow the updating of the pwm duty cycle values displayed in the GUI

&nbsp;

![](https://i.imgur.com/CTklYAK.png)

**Figure 5:** cam_client is hooked to a callback which enters into the image processing pipeline

&nbsp;

![](https://i.imgur.com/8CZhEV9.png)

**Figure 6:** Upon finishing the image processing pipeline, the detection data is sent to the drone via ctrl_client

&nbsp;

![](https://i.imgur.com/8M41DQc.png)

**Figure 7:** pwm_status_server streams pwm duty cycle values which are read from memory

&nbsp;

![](https://i.imgur.com/F37qwFn.png)

**Figure 8:** cam_stream streams frames fetched from camera by calling camera driver’s getFrame routine.

&nbsp;

![](https://i.imgur.com/BD8ACyg.png)

**Figure 9:** ctrl_server handles requests to for ‘KILLSWITCH’ and ‘ROT’. Both involve writing received data to drone’s respective memory location.
