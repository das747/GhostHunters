#include <Servo.h>

const byte FRST_M = 4, US = 2, V_SERV = 10, H_SERV = 9;
byte com = 0, move_count = 0;

Servo h_neck, neck_v;

void setup() {
  Serial.begin(9600);
  pinMode(US, OUTPUT);
  pinMode(15, OUTPUT);
  for (int i = FRST_M; i < FRST_M + 4; i++) pinMode(i, OUTPUT);
  neck_v.attach(V_SERV);
  h_neck.attach(H_SERV);
  neck_v.write(150);
  h_neck.write(90);
}

void loop() {
  if (Serial.available()) {
    com = Serial.read();
    switch (com) {
    case 5:
      turn(1);
      delay(300);
      h_neck.write(90);
      delay(300);
      next_box(60, 1);
      move_count += 1;
      delay(300);
      h_neck.write(0);
      delay(300);
      turn(0);
      break;
    case 6:
      h_neck.write(90);
      turn(1);
      back(move_count, 60);
    case 7:
      turn(0);
      break;
    case 8:
      turn(1);
      break;
    case 9:
      Serial.write(1);
      while(not Serial.available()){
      }
      move_count = Serial.read();
      break;
     default:
      sound(com);
      break;
    }
    Serial.write(1);
  }
  //    next_box(10, 1);
}

int get_us(int trig, int echo) {
  int res = 0;
  for (int i=0; i<5; i++){

    digitalWrite(trig, LOW); //НАЧАЛО ПОЛУЧЕНИЯ ДАННЫХ С US ДАТЧИКА
    delayMicroseconds(5);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW); //КОНЕЦ ПОЛУЧЕНИЯ ДАННЫХ С US ДАТЧИКА
    int value = pulseIn(echo, HIGH); //НАЧАЛО ОБРАБОТКИ ПОКАЗАНИЙ US
    value = (value / 2) / 29.1;      //КОНЕЦ ОБРАБОТКИ ПОКАЗАНИЙ US
    if (value <= 0) value = 0;
    res += value;
  }
  return int(res / 5);
}



bool next_box(int lim, bool dir) {
  while ((get_us(US, US + 1) <= lim) and (get_us(15, 14) <= lim)) {
    digitalWrite(4, !dir);
    digitalWrite(5, dir);
    digitalWrite(6, dir);
    digitalWrite(7, !dir);
  }
  stop();
  sound(1);
  while (get_us(US, US + 1) > lim or get_us(15, 14) > lim) {
    digitalWrite(4, !dir);
    digitalWrite(5, dir);
    digitalWrite(6, dir);
    digitalWrite(7, !dir);
  }
  stop();
  sound(1);
  //  delay(100);
  return 1;
}

bool back(byte n, byte lim){
  bool dir = 0;
  for (n; n > 0; n--){
    while ((get_us(US, US + 1) <= lim) or (get_us(15, 14) <= lim)) {
      digitalWrite(4, !dir);
      digitalWrite(5, dir);
      digitalWrite(6, dir);
      digitalWrite(7, !dir);
    }
    stop();
    sound(1);
    while (get_us(US, US + 1) > lim or get_us(15, 14) > lim) {
      digitalWrite(4, !dir);
      digitalWrite(5, dir);
      digitalWrite(6, dir);
      digitalWrite(7, !dir);
    }
    stop();
    sound(1);
  }
}

bool sound(byte n) {
  for (n; n > 0; n--) {
    tone(11, 300, 500);
    delay(1000);
  }
  return 1;
}

bool turn(bool dir){
  digitalWrite(4, !dir);
  digitalWrite(5, dir);
  digitalWrite(6, !dir);
  digitalWrite(7, dir);
  delay(200);
  while(digitalRead(8)){}
  stop();
}

//bool turn(int ms){
//  bool dir = ms > 0;
//  ms = abs(ms);
//  digitalWrite(4, !dir);
//  digitalWrite(5, dir);
//  digitalWrite(6, !dir);
//  digitalWrite(7, dir);
//  delay(ms);
//  stop();
//}

void stop(){
  digitalWrite(4, 0);
  digitalWrite(5, 0);
  digitalWrite(6, 0);
  digitalWrite(7, 0);
  return;
}

