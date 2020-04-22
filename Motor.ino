//////////////////////////////////////////ABOUT////////////////////////////////////////////////
//                                                                                           //
//                 This is the Arduino Code for the Self Driving Car Project.                //
//                                                                                           //
//  This code was written by Kishore K and Adithya U R from Madras Institute of Technology.  //
//                                                                                           //
//                  Please give due credit while using it in your project.                   //
//                                                                                           //
////////////////////////////////////////INITIALISATION/////////////////////////////////////////
long int mot;                                                                                //This is the value used to alter the speed of the motor.
char x;                                                                                      //Character Variable used in Serial Communication.
String val="";                                                                               //String variable used to stack all the characters received
int val_1,val_2;                                                                             //Values used control the PWM percentage of the motor pulse.
///////////////////////////////////SETTING UP THE GPIO PINS////////////////////////////////////
void setup() {                                                                               //This part of the code runs only once.
Serial.begin(9600);                                                                          //Set up serian communication with transfer speed of 9600 bps.
pinMode(2,OUTPUT);                                                                           //This is connected to -ve terminal of the right motor.
pinMode(3,OUTPUT);                                                                           //This is connected to -ve terminal of the left motor.
pinMode(4,OUTPUT);                                                                           //This is connected to +ve terminal of the right motor.
pinMode(5,OUTPUT);                                                                           //This is connected to +ve terminal of the left motor.
pinMode(10,OUTPUT);                                                                          //Used to alter the PWM percentage of the right motor.
pinMode(11,OUTPUT);                                                                          //Used to alter the PWM percentage of the left motor.
digitalWrite(2,LOW);                                                                         //Initially the right motor is at rest.
digitalWrite(3,LOW);                                                                         //Initially the left motor is at rest.
digitalWrite(4,LOW);                                                                         //Initially the right motor is at rest.
digitalWrite(5,LOW);                                                                         //Initially the left motor is at rest.
}                                                                                            //
/////////////////////////////////////////CONTROL LOOP//////////////////////////////////////////
void loop() {                                                                                //This part of the code runs in a loop indefinitely.
  while (Serial.available())                                                                 //While there are characters available in the Serial buffer.
  {                                                                                          //
    x=Serial.read();                                                                         //Read the character sent by Jetson Nano.
    if (x == ',')                                                                            //If the character is a comma, the complete value is sent.
    {                                                                                        //
      mot = val.toInt();                                                                     //Convert the received string to an integer.
      mot = map(mot,0,1023,0,160);                                                           //The value between 0-1023 is converted to a value between 0-160 for PWM.
      if (mot<80)                                                                            //If the converted value is lesser than 80,the car should go right.
      {                                                                                      //
        val_1 = 80+80-mot;                                                                   //The PWM value for the left motor(+160 to 0).
        val_2 = 3*mot-160;                                                                   //The PWM value for the right motor(+80 to -80).
        if (val_1 >= 0)                                                                      //If this value is +ve, the left wheel rotates in forward direction.
        {                                                                                    //
        digitalWrite(5,HIGH);                                                                //If the positive terminal is high.
        digitalWrite(3,LOW);                                                                 //If the negative terminal is low.
        }                                                                                    //
        if (val_2<0)                                                                         //If this value is -ve, the right motor moves backward.
        {                                                                                    //
        digitalWrite(4,LOW);                                                                 //The +ve terminal is low.
        digitalWrite(2,HIGH);                                                                //The -ve terminal is high.
        }                                                                                    //
        else                                                                                 //If the value is +ve, the right motor moves forward.
        {                                                                                    //
        digitalWrite(2,LOW);                                                                 //The -ve terminal is low.
        digitalWrite(4,HIGH);                                                                //The +ve terminal is high.
        }                                                                                    //
        analogWrite(11,val_1);                                                               //PWM value for left motor.
        analogWrite(10,abs(val_2));                                                          //PWM value for right motor.
      }                                                                                      //
      else                                                                                   //If the value is greater than 80, the car should go left.
      {                                                                                      //
        val_2 = mot;                                                                         //The PWM value for the right motor. 
        val_1 = 320-3*mot;                                                                   //The PWM value for the left motor.
        if (val_2 >= 0)                                                                      //If this value is positive, the right motor moves forward.
        {                                                                                    //
        digitalWrite(4,HIGH);                                                                //The positive terminal is high.
        digitalWrite(2,LOW);                                                                 //The -ve terminal is low.
        }                                                                                    //
        if (val_1 <0)                                                                        //If this value is -ve, the left motor moves backward.
        {                                                                                    //
        digitalWrite(5,LOW);                                                                 //The +ve terminal is low.
        digitalWrite(3,HIGH);                                                                //The -ve terminal is highe.
        }                                                                                    //
        else                                                                                 //If the value is +ve, the left motor moves forward.
        {                                                                                    //
        digitalWrite(3,LOW);                                                                 //The -ve terminal is low.
        digitalWrite(5,HIGH);                                                                //The +ve terminal is high.
        }                                                                                    //
        analogWrite(11,abs(val_1));                                                          //Setting the speed of the left motor.
        analogWrite(10,val_2);                                                               //Setting the speed of the right motor.
      }                                                                                      //
      val="";                                                                                //Reset the string to acquire the next value.
    }                                                                                        //
    else                                                                                     //If the character received from Jetson Nano is not a comma,
                                                                                             //the complete value is yet to be sent
    {                                                                                        //
      val+=x;                                                                                //Append the received character to the string.
    }                                                                                        //
  }                                                                                          //
   }                                                                                         //
///////////////////////////////////////////////////////////////////////////////////////////////
