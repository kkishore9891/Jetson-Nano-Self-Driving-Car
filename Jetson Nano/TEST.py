##########################################ABOUT##########################################
# 											#
#              This is the code used for steering the self driving car.                	#
# 											#
#      This code was written by Kishore Kumar from Madras Institute of Technology.	#
# 											#
#	         Please give due credit while using it in your project. 		# 													
# 											#
##############################IMPORTING ESSENTIAL LIBRARIES##############################
import cv2 										#For working with images.
import serial 										#For communicating with Arduino UNO.
import numpy as np 									#For working with arrays and matrices.
import time 										#For creating a time delay.
import tensorflow as tf 								#For deep learning.
import keyboard 									#For monitoring the keypresses.
from threading import Thread 								#For performing multi-threading.
######################################INITIALISATION#####################################
interpreter = tf.lite.Interpreter(model_path="Models/STEER_LITE.tflite") 		#Load the TF lite model into the program.
ser=serial.Serial("/dev/ttyACM0") 							#Establish serial communication with Arduino UNO through port ttyACM0.
											#
class CAM:										#Class to perform image capture as a seperate thread.
    def __init__(self): 								#Class constructor.
        self.ret=False 									#Initial value of ret is false.
        self.read=np.zeros((128,128,3),np.uint8) 					#Initially the image is pitch black.
    def IMG(self,cap): 									#Image capture function.
        while True: 									#Infinite loop.
            self.ret,self.read = cap.read() 						#Obtain the image from the camera.
											#
CAP = CAM() 										#Create a class object.
cap = cv2.VideoCapture(0) 								#Create a video capture object linked to first USB camera.
p_thread = Thread(target = CAP.IMG, args = (cap,)) 					#Create a thread to run the image capture function to eliminate buffering.
p_thread.daemon = True 									#This will allow the main program to exit. Otherwise the infinite loop in the thread won't stop.
p_thread.start() 									#Begin the image capture thread.
time.sleep(2) 										#Wait for 2 seconds.
interpreter.allocate_tensors() 								#Allocate tensors for the tflite model.
input_details = interpreter.get_input_details() 					#Get the input tensor.
output_details = interpreter.get_output_details()                                   	#Get the output tensor.
input_shape = input_details[0]['shape'] 						#Get the shape of the input.
											#
def show_camera(): 									#This function captures and stores the training inputs and targets
    if cap.isOpened(): 									#If the video feed is available.
        window_handle = cv2.namedWindow("FEED", cv2.WINDOW_AUTOSIZE) 			#Create a resizable window with the name Camera Feed
        angle=512 									#This the PWM value to be sent to arduino. It is initialised to 512(Forward).
        while True: 									#Infinite loop.
            img = CAP.read 								#Obtain the image from the thread. This eliminates a lag in the video feed.
            rows,cols,channels = img.shape						#Obtain the image dimensions.
            img=cv2.resize(img,(128,128)) 						#Reshape the image to a 128x128 image.
            cv2.imshow("FEED",img) 							#Display the resized image.
            cv2.waitKey(1) 								#Wait for 1 millisecond before a key is pressed.
            img=img.reshape(1,128,128,3).astype(np.float32) 				#Reshape the image and convert it to float to make it suitable for the neural network.
            interpreter.set_tensor(input_details[0]['index'], img)			#Feed the input image into the tflite model. (NOT SURE)
            interpreter.invoke()                    					#Feed forward the image down the model. (NOT SURE)
            output_data = interpreter.get_tensor(output_details[0]['index']) 		#Obtain the result. (NOT SURE)
											#
            if keyboard.is_pressed('esc'): 						#If the escape key is pressed.
                break          								#Terminate the loop.
            angle = int(output_data*1023) 						#Denormalise the output value(0-1) back to the value to be sent to arduino(0-1023)
            print("Angle:",angle) 							#Print the output value.
            ser.write((str(angle)+",").encode()) 					#Send the value to arduino along with a comma to help is decode the angle.
        cap.release() 									#Close the camera.
        cv2.destroyAllWindows() 							#Close the video feed.   
##################################RUNNING THE PROGRAM####################################
if __name__ == "__main__": 								#This block won't run if imported from a different program.
    show_camera() 									#The program loop is executed.
    ser.close() 									#Stop the serial communication.
    ser=serial.Serial("/dev/ttyACM0") 							#For a connection once again with arduino. This resets the arduino and the car will stop.
    ser.close() 									#Stop the serial communication once again.
#########################################################################################    

