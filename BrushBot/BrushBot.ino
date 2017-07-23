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
const char* ssid = "GRITS_Lab";
const char* password = "grits434!";
unsigned int localUdpPort = 8888;
char receivedPacket[255];
WiFiUDP Udp;

//Motor Variables
const int leftMotorPin = 2;
const int rightMotorPin = 13;

//Ultrasonic Variables
const int trigPin = 12;
const int echoPin = 14;
const int maxDistance = 200;
long distance;
NewPing sonar(trigPin, echoPin, maxDistance);

//IMU Variables
long gyroZ;
float accelY;
LSM6DS3 brushBotIMU;

void setup() {
  //Initialize Pins and IMU.
  pinMode(leftMotorPin, OUTPUT);
  pinMode(rightMotorPin, OUTPUT);
  brushBotIMU.begin();
  
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
  gyroZ = brushBotIMU.readFloatGyroZ();

  //Read accelerometer data
  accelY = brushBotIMU.readFloatAccelY();
  
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
    String leftMotor;
    String rightMotor;
    for(int i = 0;i < strlen(receivedPacket);i++){
      if (receivedPacket[i] == ' '){
        char left[i];
        char right[strlen(receivedPacket)-i];
        strncpy(left, receivedPacket,i);
        strncpy(right, receivedPacket+i,strlen(receivedPacket));
        leftMotor = String(left);
        rightMotor = String(right);
      }
    }
    
    int l = leftMotor.toInt();
    int r = rightMotor.toInt();
    analogWrite(leftMotorPin,l);
    analogWrite(rightMotorPin,r);
    Serial.println(analogRead(leftMotorPin));
  }
}
