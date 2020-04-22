# Jetson-Nano-Self-Driving-Car
   This is a project which uses deep Convolutional Neural Networks to steer a self driving car. It is powered by Jetson Nano and Arduino UNO.

<p align="center">
   
  <img width="300" height="275" src="https://user-images.githubusercontent.com/34810513/79965877-38c59100-84aa-11ea-9d23-f7f33091443c.jpeg">
  
</p>


   Neural networks are universal function approximators which can be used for different kinds of problems(Classification, Regression, Segmentation, etc). In this self driving car prototype, I have used regression(I have tried classification too but regression is the way to go) to predict the steering angle of a car by using the video feed of the path as input to the neural network. Use this GitHub Repo to help build your own Self Driving Car. You can also alter the code slightly to use a car with Ackerman Steering and Servo Motors instead of using the classic Line Follower styled Chassis that I have used. With that being said, lets get started.


## The Self Driving Car Concept

   This self driving car is a robot with four wheels powered by Arduino UNO, a Motor driver, a LIPO battery, 4 motors and wheels. The intelligent operations are carried out by NVIDIA's Jetson Nano board, which is a single board computer with GPU cores and CUDA support. The Jetson board processes the images obtained in real time from a web camera and feeds them into a Neural network with convolutional and fully connected layers. The neural network performs regression to predict the steering angle of the car and the angle is used to control the speed of the wheels of the robot, which makes it turn left, right or forward.

   To understand this, consider a computer game where a user can drive a car by pressing the arrow keys. In order for an AI to drive the car, it should be able to predict the key to be pressed and the duration for which the key should be pressed based on the steering angle. To do this, it obtains a screen shot of the game for every fraction of a second and passes it through a neural network. The neural network predicts the steering angle at that instant and the AI presses the appropriate key. This keeps the car at the center of the road as shown below.

<p align="center">
  <img width="325" height="200" src="https://user-images.githubusercontent.com/34810513/79974333-c3ac8880-84b6-11ea-8b67-1ee88e75583c.jpeg">
</p>

   Instead of making the AI drive the car in a computer game, we use real world data obtained from a robotic car prototype. The AI processes the real world feed and keeps the prototype at the center of the lane. We have used the following architecture which consists of 4 Convolutional layers, 1 fully connected layer and 1 output neuron which predicts the normalised steering angle.
   
<p align="center">
  <img width="1062" height="275" src="https://user-images.githubusercontent.com/34810513/79981811-ecd31600-84c2-11ea-9431-555dff3b42dc.jpg">
</p>

## Components And Connections

We used the following components to build our prototype:
 
 1) Eagle high discharge LIPO Battery (11.1V, 35C) - 1 pc.
 2) IC-7805 regulators - 4pcs.
 3) L298N motor driver module - 1 pc.
 4) 300 RPM Motors - 4 pcs.
 5) Arduino UNO - 1 pc.
 6) NVIDIA Jetson Nano board - 1 pc.
 7) I-Ball Web Camera - 1 pc.
 8) Metal Chassis - 1 pc.
 9) Wheels - 4 pcs.
 10) Wires and Jumper Cables - as per required.
 11) Metal spacers - 4 pcs
 12) Perf Board - 1
 13) Wireless Keyboard and Mouse.
 14) Wifi adapter chip for Jetson Nano(Optional).
 
 #### Custom regulator circuit
 
   The Jetson Nano board is a troublesome board. There are 2 major ways through which you can power the board. The first method is to use a 10W micro USB mobile charger and power the board through its micro USB port. Though this is handy and quick, it is not the best way to power the board. Although we can make the project portable using powerbanks, the board automatically switches off when the pwoer drawn by it exceeds 10 Watts. This makes it virtually impossible to use it for projects like our self driving car. Thus, the DC barrel Jack of Jetson Nano can be used to power the board. To do so, a small jumper should be fit into Jetson's J48 pins(For more info visit: https://www.jetsonhacks.com/2019/04/10/jetson-nano-use-more-power/). Once this is ready, we have to power the Jetson board using the LIPO battery. The LIPO battery is powerful and allows high current discharge. However, it supplies a voltage of 11V which will damage the board. This is why we need the 4 regulator ICs each IC has a maximum current rating of 1.5A. Thus connecting 4 of them in parralel lets us draw around 4 Amps of current with a voltage of 5V(20 Watts). This Acts as a stable power supply which can be used in our project.

<p align="center">
<img width="275" height="250" src="https://user-images.githubusercontent.com/34810513/79977737-5f8cc300-84bc-11ea-94d3-12505b291ee8.jpg">
<img width="275" height="250" src="https://user-images.githubusercontent.com/34810513/79977923-b5616b00-84bc-11ea-901e-10539c5d49f6.jpeg">
<img width="275" height="250" src="https://user-images.githubusercontent.com/34810513/79978174-14bf7b00-84bd-11ea-8610-51e7a5e3629b.jpeg">
</p> 

<p align="center">
  The custom regulator circuit. a) Circuit Diagram (Left) b) Top View (Center) c) Bottom View (Right)
</p>

#### The Complete Circuit

   Once the custom regulator circuit is ready, it is time to build the complete circuit. Use the circuit diagram shown below to make the connections. In addition to this, connect Motors 3 and 4 in parallel with motors 1 and 2 respectively. The spacers can be elevate the position of the Jetson board which makes it easier to fit all the components onto a small chassis. Feel free to tinker with the design.
   
<p align="center">
  <img width="580" height="640" src="https://user-images.githubusercontent.com/34810513/79979248-d925b080-84be-11ea-9f89-b81b1eadd50b.jpeg">
</p>

## Using the Code

After making the connections as shown above, it is time to setup the software of the Self Driving Car. There are 3 folders in the repository.

1) Arduino Code
2) Jetson Nano
3) PC

Just as the name suggests, each folder contains codes to be run in Arduino UNO, Jetson Nano and the PC respectively. Follow the procedure to get the self driving car up and running.

#### 1. Download the repository

This is the most simple and obvious step. Download the repository into your PC using the git command or the download option. All the folders have already been arranged for you in a way that the codes will run seamlessly. Copy the PC folder into you PC and Jetson Nano folder into your Jetson Board.

#### 2. Upload the Arduino Code

Once you have downloaded the repo, connect the Arduino UNO to your PC and flash Motor.ino into it using the Arduino IDE. This code communicates with the Jetson Nano board using serial communication and controls the speeds of the motors.

#### 3. Collect the Training data

Now that the Arduino Code is ready, it is time to drive the car and collect the training data. Make your own track using A4 sheets or a flex banner with a track printed on it. Make sure that the "Images" folder and RECORD.py exist in the same folder and run RECORD.py program from terminal. The car starts to move after pressing either of the w a or d keys. To turn left press a, to turn right press d and to go forward press either w or press nothing. The car moves forward by default. Drive the car for atleast 20 laps to collect a decent amount of data to train the model. Make sure that the car has equal number of left and right turns and straight roads occasionally to acquired a robust data with all possible inputs and outputs. Press the "Esc" key to terminate the program. Open the images folder to look at all the images. The Targets.txt contains the respective steering angles for each images in a sequence.

#### 4.Prepare the Dataset

Copy the Images folder and Target.txt file to the PC folder. Run DATA.py to convert the images into a .npy file containing Inputs and targets to train the neural network. The program creates both the balanced and unbalanced datasets. Use the balanced dataset available in the "Datasets" folder to train the model. This reduces the possibility of overfitting the neural network.

#### 5. Train the Model

Run MODEL.py to run the training program. This code create a custom neural network with the architecture specified above and train it for 30 epochs. To prevent overfitting it uses validation data and performs checkpointing. The models are saved in Models/Model HDF5/Regression by default. The finally created model is the most accurate model. The model makes predictions as shown below. You will see the model returning the steering angles instead of displaying Left, Right or Forward as shown here.

<p align="center">
  <img width="250" height="100" src="https://user-images.githubusercontent.com/34810513/79984783-46d5da80-84c7-11ea-9d37-5f3076d8b092.gif">
</p>


#### 6. Convert the model to a TF-Lite model

Run CONVERT.py to convert the hdf5 tensorflow model to a TF-Lite model. This quantises the hdf5 model by converting the weight from float to int. This retains the accuracy of the mode while making it much lighter. This allows Jetson Nano to perform the computations much faster than the usual. The TF Lite model is saved in Models/TF Lite Models.

#### 7. Run the testing program.

Once the TF Lite Model is ready, copy the model into the Jetson Nano/Models folder in your Jetson Nano and run the TEST.py program.




