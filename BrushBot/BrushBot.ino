#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <string.h>
#include <stddef.h>
#include <stdio.h>
#include "FS.h"

const char* ssid = "GRITS_Lab";
const char* password = "grits434!";
char reply[] = "1.5 2.0 4.0 1";
WiFiUDP Udp;
unsigned int localUdpPort = 8888;
char receivedPacket[255];

int leftMotorPin = 16;
int rightMotorPin = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(leftMotorPin, OUTPUT);
  pinMode(rightMotorPin, OUTPUT);
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

void writePacket(char s[]){
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
  Udp.write(s);
  Udp.endPacket();
}

void loop() {
  // put your main code here, to run repeatedly:
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
    //int l = atoi(leftMotor);
    int r = atoi(rightMotor);
    //Serial.print(l + " ");
    Serial.println(r);
    digitalWrite(r,rightMotorPin);
    digitalWrite(r,leftMotorPin);
    
  }
}
