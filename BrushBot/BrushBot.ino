#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <string.h>
#include <stddef.h>
#include <stdio.h>
#include <NewPing.h>
#include "FS.h"
#include "SparkFunLSM6DS3.h"
#include <math.h>

//WiFi Variables
const char* ssid = "TCONTIS";
const char* password = "qazxswedc";
unsigned int localUdpPort = 8888;
char receivedPacket[255];
WiFiUDP Udp;

//Motor Variables
const int leftEnable = 5; //D1
const int leftInputA = 4; //D2
const int leftInputB = 0; //D3
const int rightEnable = 15; //D8
const int rightInputA = 13; //D7
const int rightInputB = 2; //D4

//Ultrasonic Variables
const int trigPin = 12; //D6
const int echoPin = 14; //D5
const int maxDistance = 200;
long distance;
NewPing sonar(trigPin, echoPin, maxDistance);

//IMU Variables
long gyroZ;
float accelY;
//LSM6DS3 brushBotIMU;

void setup() {
  //Initialize Pins and IMU.
  pinMode(leftEnable, OUTPUT);
  pinMode(leftInputA, OUTPUT);
  pinMode(leftInputB, OUTPUT);
  pinMode(rightEnable, OUTPUT);
  pinMode(rightInputA, OUTPUT);
  pinMode(rightInputB, OUTPUT);
  //brushBotIMU.begin();
  
  //Begin serial communication and attempt to connect to wifi
  Serial.begin(115200);
  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
  Udp.begin(localUdpPort);
  
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
}

//Set H-bridge pins based on speed and direction
void setMotor(int speedNumber, int enablePin, int inputAPin, int inputBPin){
  analogWrite(enablePin, abs(speedNumber));
  if (speedNumber < 0){
    digitalWrite(inputAPin, LOW);
    digitalWrite(inputBPin, HIGH);
  }
  else if (speedNumber > 0){
    digitalWrite(inputAPin, HIGH);
    digitalWrite(inputBPin, LOW);
  }
  else{
    digitalWrite(inputAPin, LOW);
    digitalWrite(inputBPin, LOW);
  }
}

//Void to write packet to address.
void writePacket(char s[]){
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.write(s);
  Udp.endPacket();
}

void loop() {
  //Read Ultrasonic data in centimeters
  distance = sonar.ping_cm();

  //Read gyro data
  gyroZ = 0;//brushBotIMU.readFloatGyroZ();

  //Read accelerometer data
  accelY = 0;//brushBotIMU.readFloatAccelY();
  
  // put your main code here, to run repeatedly:
  char reply[32];
  char reply2[32];
  char reply3[32];
  sprintf(reply, "%d ", distance);
  sprintf(reply2, "%d ",gyroZ);
  dtostrf(accelY, 3, 5, reply3);
  char rep[255] = "";
  strcat(reply, reply2);
  strcat(reply, reply3);
  int packetSize = Udp.parsePacket();
  if (packetSize){
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(receivedPacket, 255);
    if (len > 0)
    {
      receivedPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", receivedPacket);
    writePacket(reply);
    char leftMotor[20];
    char rightMotor[20];
    for(int i = 0;i < strlen(receivedPacket);i++){
      if (receivedPacket[i] == ' '){
        strncpy(leftMotor, receivedPacket,i);
        strncpy(rightMotor, receivedPacket+i,strlen(receivedPacket));
      }
    }
    
    int l = atoi(leftMotor);
    int r = atoi(rightMotor);
    Serial.print(l);
    Serial.print(" ");
    Serial.println(r);
    setMotor(l, leftEnable, leftInputA, leftInputB);
    setMotor(r, rightEnable, rightInputA, rightInputB);
  }
}
