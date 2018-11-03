#include <Arduino.h>
#include <WiFi.h>
#include "SSD1306Wire.h"


const char* ssid     = "BrainPatch";
const char* password = "brain";

#define LED_PIN 23

SSD1306Wire  display(0x3c, 5, 4);
// Initialize web server on 80th port
WiFiServer server(80);

int freq = 5000;
int ledChannel = 0;
int resolution = 8;

// Function to change IP to string variable
String IpAddress2String(const IPAddress& ipAddress)
{
  return String(ipAddress[0]) + String(".") +\
  String(ipAddress[1]) + String(".") +\
  String(ipAddress[2]) + String(".") +\
  String(ipAddress[3])  ;
}

void write2(int dutyCycle){
  ledcWrite(ledChannel, dutyCycle);
}

void setup() {
  Serial.begin(115200);
  Serial.println("Ping");
  display.init();
  display.flipScreenVertically();
  display.clear();
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.setFont(ArialMT_Plain_10);
  display.drawString(0, 0, "Brain Patch");
  display.drawString(0, 10, "Cleverest Technologies");
  display.drawString(0, 20, "BraniacDog");
  display.drawString(0, 30, "brainpatch.ai");
  display.display();
  // Create access point
  WiFi.softAP(ssid, password);
  // Begin server
  server.begin();
  String IP2 = IpAddress2String(WiFi.softAPIP());
  Serial.print("My IP is: ");
  Serial.println(IP2);
  Serial.println(WiFi.softAPIP());
  display.drawString(0, 40, IP2);
  display.display();
  pinMode(25, OUTPUT);
}

void loop() {
    WiFiClient client = server.available();   // listen for incoming clients

    if (client) {                             // if you get a client,
      Serial.println("New Client.");           // print a message out the serial port
      String currentLine = "";                // make a String to hold incoming data from the client
      while (client.connected()) {            // loop while the client's connected
        if (client.available()) {             // if there's bytes to read from the client,
          char c = client.read();             // read a byte, then
          Serial.write(c);                    // print it out the serial monitor
          if (c == '\n') {                    // if the byte is a newline character

            // if the current line is blank, you got two newline characters in a row.
            // that's the end of the client HTTP request, so send a response:
            if (currentLine.length() == 0) {
              // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
              // and a content-type so the client knows what's coming, then a blank line:
              client.println("HTTP/1.1 200 OK");
              client.println("Content-type:text/html");
              client.println();

              // the content of the HTTP response follows the header:
              client.print("Click <a href=\"/0\">here</a> to go<br>");
              client.print("Click <a href=\"/1\">here</a> to stop<br>");

              // The HTTP response ends with another blank line:
              client.println();
              // break out of the while loop:
              break;
            } else {    // if you got a newline, then clear currentLine:
              currentLine = "";
            }
          } else if (c != '\r') {  // if you got anything else but a carriage return character,
            currentLine += c;      // add it to the end of the currentLine
          }

          // Check to see if the client request was "GET /H" or "GET /L":
          if (currentLine.endsWith("GET /1")) {
            digitalWrite(25, LOW);
            Serial.println("STOP!");

          }
          if (currentLine.endsWith("GET /0")) {
            digitalWrite(25, HIGH);
            }
        }
      }
      // close the connection:
      client.stop();
  }
}
