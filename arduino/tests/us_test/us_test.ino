void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);  //trig
  pinMode(17, OUTPUT);
}

void loop() {
  Serial.println((String) get_us(7, 8) + '\t' + get_us(17, 18));
}

int get_us(int trig, int echo){
  digitalWrite(trig, LOW); 
  delayMicroseconds(5);
  digitalWrite(trig, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trig, LOW); 
  int value = pulseIn(echo, HIGH);
  value = (value/2) / 29.1;
  if(value<=0) value=1000;
  delay(2);
  return value;
}
