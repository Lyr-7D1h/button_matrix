#include <Arduino.h>

const int pins[8] = {15,2,4,16,17,5,18,19};

void setup() {
    Serial.begin(115200); // Matches monitor_speed
  for (int i = 0; i < 4; i++) {
    pinMode(pins[i], OUTPUT); 
    digitalWrite(pins[i], HIGH); 
  }
  for (int i = 4; i < 8; i++) {
    Serial.println(pins[i]);
    pinMode(pins[i], INPUT_PULLUP); 
  }
}

void loop() {
  for (int r = 0; r < 4; r++) {
    digitalWrite(pins[r], LOW); 
    for (int c = 4; c < 8; c++) {
      if (digitalRead(pins[c]) == LOW) { 
        Serial.print("Button Pressed: ");
        Serial.println("r: " + String(r) + " c: " + String(c % 4));
        while (digitalRead(pins[c]) == LOW) {
          delay(10); 
        }
      }
    }
    digitalWrite(pins[r], HIGH); 
  }
}
