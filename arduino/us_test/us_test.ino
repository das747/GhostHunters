void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);  //trig
  pinMode(15, OUTPUT);
}

void loop() {
  Serial.println(get_us(2, 3) + '\t' + get_us(15, 14));
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
