##################################ABOUT##################################################
# 									                #
#   This is the code used for collecting the training data for the self driving car.    #
# 											#
#     This code was written by Kishore Kumar from Madras Institute of Technology.	#
# 											#
#	         Please give due credit while using it in your project. 		# 													
# 											#
##############################IMPORTING ESSENTIAL LIBRARIES##############################
import cv2              								#For working with images.
import serial 										#For communicating with Arduino UNO.
import numpy as np 									#For working with vectors and matrices.
import keyboard  									#For monitoring key presses.
######################################INITIALISATION#####################################
ser=serial.Serial("/dev/ttyACM0") 							#Serial object to communicate with arduino through ttyACM0 port.
file = open("Target.txt","w") 								#This text file contains the target values.
#######################################PROGRAM LOOP######################################
def show_camera():									#This function captures and stores the training inputs and targets. 
    cap = cv2.VideoCapture(0) 								#Create a video capture object linked with the first USB camera.
    if cap.isOpened(): 									#If the video feed is available.
        window_handle = cv2.namedWindow("Camera Feed", cv2.WINDOW_AUTOSIZE)		#Create a resizable window with the name Camera Feed
        angle=512 									#This the PWM value to be sent to arduino. It is initialised to 512(Forward).
        ctr=0 										#Counter variable to store the images.
        while True: 									#Infinite Loop.
            ret_val, img = cap.read() 							#Obtain the image from the camera.
            rows,cols,channels = img.shape						#Obtain the image dimensions.
            cv2.imshow("Camera Feed", img) 						#Display the image.
            cv2.waitKey(30) 								#Wait for 30 milliseconds before a key is pressed.
            if keyboard.is_pressed('esc'): 						#If escape key is pressed.
                break 									#Terminate the program loop.
            elif keyboard.is_pressed('d'): 						#If d is pressed. 
                angle-=100 								#Decrement the current angle value by 100 (Right).
            elif keyboard.is_pressed('a'):						#If a is pressed.
                angle+=100 								#Increment the current angle value by 100 (Left).
            elif keyboard.is_pressed('w'): 						#If w is pressed.
                angle=512 								#Replace the current angle by 512 (Forward).
            else: 									#If nothing is pressed.
                angle=512 								#Replace the angle by 512 (Forward).
            print("Value:", angle)            						#Display the value.
            ser.write((str(angle)+",").encode()) 					#Send the angle value as a byte stream along with a comma to help arduino decode it.
            try: 									#This prevents the code from crashing due to error.
                file.write("Target "+str(ctr)+":"+str(angle)+"\n") 			#Append the angle value to the targets text file.
                cv2.imwrite("Images/"+str(ctr)+".jpg",img) 				#Save the nth image in the Images folder.
                ctr+=1 									#Increment the counter variable.
            except: 									#If the block has an error,
                pass 									#Do nothing.
        cap.release() 									#Close the camera object.
        cv2.destroyAllWindows() 							#Close the video feed.
        file.close() 									#Close and save the text file.
###################################RUNNING THE PROGRAM###################################
if __name__ == "__main__": 								#This block won't run if imported from a different program.
    show_camera() 									#The program loop is executed.
    ser.close() 									#Stop the serial communication.
    ser=serial.Serial("/dev/ttyACM0") 							#For a connection once again with arduino. This resets the arduino and the car will stop.
    ser.close() 									#Stop the serial communication once again.
#########################################################################################    

