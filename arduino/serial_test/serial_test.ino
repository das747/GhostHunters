void setup() {
  Serial.begin(9600);
}

void loop() {
  if(Serial.available()){
    byte com = Serial.read();
    com += 2; // любое действие
    Serial.write(com); //не print
  }
}
