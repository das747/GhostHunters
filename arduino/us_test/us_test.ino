void setup() {
  Serial.
  pinMode(2, OUTPUT);  //trig
}

void loop() {
  Serial.println(get_us(2, 3));
  delay(100);
}

int get_us(int trig, int echo){
  digitalWrite(trig, LOW); 
  delayMicroseconds(5);
  digitalWrite(trig, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trig, LOW); 
  int value = pulseIn(echo, HIGH);
  value = (value/2) / 29.1;
  if(value<=0) value=0;
  return value;
}
