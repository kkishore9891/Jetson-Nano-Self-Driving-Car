#################################################ABOUT###############################################
#         	 	This code converts the a model from tf to tflite for Jetson Nano.        			#
# 																									#
#			This code was written by Kishore Kumar from Madras Institute of Technology.				#
# 																									#
#	                 Please give due credit while using it in your project. 						#	
# 																									#
#####################################IMPORTING ESENTIAL LIBRARIES####################################
from tensorflow import keras 																		#For loading the hdf5 Model.
import tensorflow.lite as lite 																		#For converting the model to tflite version.
model = keras.models.load_model("Models/Models HDF5/Regression/weights-improvement-21-0.00.hdf5") 	#Load the hdf5 model.
model.save("Models\\Models\\STEER.model") 															#Save it as .model file.
model = keras.models.load_model("Models/Models/STEER.model") 										#Load the new model.
converter = lite.TFLiteConverter.from_keras_model(model) 											#Prepare a tflite converter for the new model.
tflite_model = converter.convert() 																	#Convert it into a tflite bytestream file.
open("Models/TF Lite Models/STEER_LITE.tflite", "wb").write(tflite_model) 							#Save the bytestream into a .tflite text file.
#####################################################################################################
