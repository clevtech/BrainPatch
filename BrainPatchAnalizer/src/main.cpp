#include <Arduino.h>

void setup() {
  Serial.begin(115200);

}

void loop() {

  if(Serial.available()){
  int val = analogRead(A0);
  Serial.println(val);
}
}
