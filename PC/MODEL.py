######################################################ABOUT######################################################
# 											                        #
#	    	      This is the code used for training the model for the self driving car. 	        	#
# 											                        #
#		   This code was written by Kishore Kumar from Madras Institute of Technology.		        #
# 											                        #
#	                       Please give due credit while using it in your project. 			        #
# 											                        #
##########################################IMPORTING ESSENTIAL LIBRARIES##########################################
import tensorflow as tf           									        #Deep learning library.
import numpy as np 										                #For processing matrices and array.
import cv2 										                        #For processing images.
from tensorflow.keras.layers import Flatten,Dense,Conv2D,MaxPool2D,Activation,Dropout 			    	#Necessary layers for constructing the model.
from tensorflow.keras.callbacks import ModelCheckpoint 						                #This is used for checkpointing the model.
keras=tf.keras 										                        #Keras model of tensorflow.
###############################################DATASET AUGMENTATION##############################################
def augment(img): 										                #Augmentation function.
  M=cv2.getRotationMatrix2D((64,64),np.random.randint(-10,10),1)					        #Matrix to randomly rotate the image anywhere by -10 to 10 degreees about the center.
  img=cv2.warpAffine(img,M,(128,128)) 								                #Rotating the image using the matrix.
  return img 										                        #Return the augmented image.
##############################################PREPARING THE DATASET##############################################
data=np.load("Datasets/TRAIN_BALANCED_STEER.npy",allow_pickle=True) 					        #Load the balanced dataset.
X=np.array([augment(x[0]) for x in data ]) 								        #Training input with augmented images.
Y=np.array([np.array(x[1]) for x in data]) 								        #Training targets.
###############################################DEVELOPING THE MODEL##############################################
model=keras.Sequential()									                #Blank model with no layers.
model.add(keras.layers.Lambda(lambda x:x/255,input_shape=(128,128,3))) 				                #This layer normalises the input images.
model.add(Conv2D(32,(3,3),padding='same')) 							                #Convolutional layer with 32 feature maps and 3x3 kernels.
model.add(Activation('relu')) 									                #ReLU activation function.
model.add(Dropout(0.3)) 									                #Neuron dropout probability is 30%.
model.add(MaxPool2D(pool_size=(2,2))) 							                        #Maxpooling layer reduces the size of the feature maps by half.
model.add(Conv2D(64,(3,3),padding='same'))							                #Convolutional layer with 64 feature maps and 3x3 kernels.
model.add(Activation('relu')) 									                #ReLU activation function.
model.add(Dropout(0.3))									                        #Neuron dropout probability is 30%.
model.add(MaxPool2D(pool_size=(2,2))) 							                        #Maxpooling layer reduces the size of the feature maps by half.
model.add(Conv2D(128,(3,3),padding='same'))							                #Convolutional layer with 32 feature maps and 3x3 kernels.
model.add(Activation('relu')) 									                #ReLU activation function.
model.add(Dropout(0.3))									                        #Neuron dropout probability is 30%.
model.add(MaxPool2D(pool_size=(2,2))) 							                        #Maxpooling layer reduces the size of the feature maps by half.
model.add(Conv2D(256,(3,3),padding='same'))									#Convolutional layer with 32 feature maps and 3x3 kernels.
model.add(Activation('relu')) 											#ReLU activation function.
model.add(Dropout(0.3))												#Neuron dropout probability is 30%.
model.add(MaxPool2D(pool_size=(2,2))) 										#Maxpooling layer reduces the size of the feature maps by half.
model.add(Flatten()) 												#Flatten the feature maps to a 1-D vector.
model.add(Dense(128)) 												#Fully connected layer with 128 neurons.
model.add(Activation("relu")) 											#ReLU activation function.
model.add(Dropout(0.3)) 											#Neuron dropout probability is 30%.
model.add(Dense(1)) 												#Output neuron to predict normalised steering angle.
model.add(Activation("sigmoid")) 										#Sigmoid activation function returns a value between 0-1.
################################################TRAINING THE MODEL###############################################
#model=keras.models.load_model("Model.model") 									#Uncomment this line to retrain a model(Change the file path).
model.compile(loss="mse",optimizer=keras.optimizers.Adam(learning_rate=0.0003),metrics=['accuracy'])		#Using Adam optmiser and mean square error to optimise the model.
filepath="Models/Models HDF5/Regression/weights-improvement-{epoch:02d}-{val_accuracy:.2f}.hdf5"                #Path to save the checkpoints.
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')		#Save the models with the lowest validation loss upto that point.
callbacks_list = [checkpoint] 											#Used in model.fit.
model.fit(X, Y, validation_split=0.30, epochs=30, batch_size=10, callbacks=callbacks_list, verbose=1)		#Train the model for 30 epochs using 30% of the data as validation data.
#################################################################################################################
