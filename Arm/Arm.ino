#include <Servo.h> 

int baseServoPin =5;
int servo1Pin=6;
int servo2Pin=10;
int servo3Pin=11;

Servo baseServo;
Servo servo1;
Servo servo2;
Servo servo3;


void setup()
{
  Serial.begin(9600);
  baseServo.attach(baseServoPin);
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  servo3.attach(servo3Pin);
}

void loop() 
{
  String uri=Serial.readString();
  moveServo(uri);
}



void moveServo(String uri)
{
  int index=uri.indexOf('/');
  int motorTomove=99;
  int angle=180;
  int angle2=180;
  motorTomove= uri.substring(0,index).toInt();
  angle=uri.substring(index+1).toInt();

  switch(motorTomove)
  {
    case 0:
      break;
    case 1: 
      baseServo.write(angle);
      break;
    case 2:
    angle2=map(angle,0,180,10,180);
      servo1.write(angle2);
      break;
    case 3:
      angle2=map(angle,0,180,10,180);
      servo2.write(angle2);
      break;
    case 4:
      servo3.write(angle);
      break;
  }
}
