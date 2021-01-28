# Gesture-Recognition-for-Touchless-Input
Hand Gesture Recognition for Touchless Utilization of Computer Systems
Pandemics give rise to concerns in the minds of people over shared contact. In places like the ATM and automated ticket vending machines in metro stations, key-pads/touchscreens are used for input. It is hard to keep such devices sanitized when they are so frequently used. To avoid keypad as input, other forms of input like audio, and use of visual input is suggested. Webcams present a cheap hardware solution that can also be easily incorporated with already existing systems, and are already built-in in a majority of personal devices. The issue with using audio as input is that it can be easily affected by external disturbances. In such cases the best alternative is a visual input using the device camera or an external camera, with live image processing.

Hence, the aim of this project is to create a program for touchless input for system controls in various specialized domains, using video input from an internal/externally connected webcam. Aside from having the advantage of contactless usage, visual input also has the advantage of being more accessible to people who are not familiar with the use of various devices. Thus, it can be considered to be useful in a variety of scenarios, such as personal home use and public machines like kiosks, ATMs etc.
Thus, the project tries to explore the use of device webcams for taking in real time input of our hands and to use this input for input in various domains of system control.

Feed Capture and Background Averaging- Capture the input from the attached webcam and calculate background, using OpenCV functions. Also flip the image using iMutils.
Thresholding and Contour Drawing. Binarize the frame with hand using threshold-ing and then draw contour along hand outline.

Segmentation and Convex Hull- Separate mask of hand using AND operation, which compares every pair of pixels in the frames. Thus, the hand is separated as it is the only difference in every frame, compared to the background. Draw circle using extreme points of segment and calculate intersections with fingers.

System Utility Controls- Track a point on hand segment for cursor control and custom file selection. Utilize finger count for volume control, brightness control and screenshot functionality.
