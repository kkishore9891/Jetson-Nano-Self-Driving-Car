##################################ABOUT#################################
# 									#
#                This is the code used for preparing the training data for the self driving car.                #
# 									#
#	This code was written by Kishore Kumar from Madras Institute of Technology.	#
# 									#
#	                 Please give due credit while using it in your project. 			# 													
# 									#
######################IMPORTING ESSENTIAL LIBRARIES######################
import numpy as np              							#For working with matrices and vectors.
import cv2 								#For processing images.
from random import shuffle 							#For shuffling the dataset.
import time 								#For inserting time delays.
##############################INITIALISATION###############################
ctr=0 									#Counter variable to scan through images.
file_name= "Datasets/Training_Data.npy" 					#File path for unbalanced data.
training_data = [] 								#List to save input and targets.
file = open("Target.txt","r") 							#This text file is obtained from Jetson Nano and it contains the steering angle value for each image.
x=file.read().split("Target")[1:] 							#Removes the word Target from each line in the txt file.
##########################DATA PROCESSING LOOP#########################
while True: 								#Infinite loop.
    img=cv2.imread("Images/"+str(ctr)+".jpg")					#Loads the nth image into the program.
    try: 									#To prevent the program from scarching due to error(Due to corrupt image files).
        image=cv2.resize(img,(128,128)) 						#Resize the image into a 128x128 image.
        cv2.imshow("Feed",image) 						#Displays the resized images (video feed).
        val=x[ctr].split(":")[1].strip() 							#Extract the target value alone from each line in the text file.
        target=int(val)/1023 							#Convert the string to an integer and normalise it to a floating point value.
        print(target) 								#Print the normalised target value.
        training_data.append([image,target]) 					#Append the input and target to the dataset list.
        if cv2.waitKey(1) == 27: 							#If escape key is pressed, quit the dataset collection.
            break 								#
        ctr += 1 								#Increment the counter variable
        if ctr >= 27838: 								#This number is the name of the last image present in the Images folder. If you numbers vary, change it accordingly.
            break 								#Once the program has scanned through all the images, quit the loop.
    except: 									#If the image is corrupted, do nothing and increment the counter.
        ctr += 1 								#
######################DATASET SAVING AND BALANCING#####################
cv2.destroyAllWindows() 							#Close the video feed.
np.save(file_name,training_data) 						#Save the unbalanced dataset.
lefts = [] 									#Array to save left images and targets.
rights = [] 									#Array to save right images and targets.
forwards = [] 								#Array to save forward images and targets.
shuffle(training_data) 							#Shuffle the dataset.
for data in training_data: 							#Loop through the data.
    img = data[0] 								#Obtain the input image.
    choice = data[1] 								#Obtain the corresponding target value.
    if choice > 0.5004887585532747: 						#If the value exceeds 0.5, the car went left.
        lefts.append([img,choice]) 							#Append the image and target into left data.
    elif choice == 0.5004887585532747:                                                          		#If the value is 0.5, the car went forward.
        forwards.append([img,choice]) 						#Append the image and target into forward data.
    elif choice < 0.5004887585532747: 						#If the value is below 0.5, the car went right.
        rights.append([img,choice]) 						#Append the image and target into right data.
    else: 									#If the data didn't fall into any of the categories.
        print('no matches') 							#Error message.
shuffle(forwards)								#Shuffle the forward data.
shuffle(lefts) 								#Shuffle the left data.
shuffle(rights) 								#Shuffle the right data.
print("BEFORE BALANCING:") 						#Display the dataset size before balancing the data.
print("FORWARD:",len(forwards)) 						#Forward data size.
print("LEFT:",len(lefts)) 							#Left data size.
print("RIGHT:",len(rights)) 							#Right data size.
forwards = forwards[:len(lefts)][:len(rights)] 					#Forward data is cut short to the shortest size.
lefts = lefts[:len(forwards)] 							#Left data is cut short to the shortest size.
rights = rights[:len(forwards)] 							#Right data is cut short to the shortest size.
print("AFTER BALANCING:") 							#Display the dataset size after balancing the data.
print("FORWARD:",len(forwards)) 						#Balanced forward data size.
print("LEFT:",len(lefts)) 							#Balanced left data size.
print("RIGHT:",len(rights)) 							#Balanced right data size.
final_data = forwards + lefts + rights 						#Prepare the final balanced dataset.
shuffle(final_data) 								#Shuffle the final data to prevent overfitting while training.
np.save('Datasets/TRAIN_BALANCED_STEER.npy', final_data) 			#Save the balanced dataset.
time.sleep(5) 								#Wait for 5 seconds.
#########################################################################



