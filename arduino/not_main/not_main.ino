#include <Servo.h>

const byte FIRST_M = 3, US = 7, US2 = 17, V_SERV = 10, H_SERV = 9;
byte com = 0, move_count = 0;

Servo h_neck, neck_v;

void setup() {
  Serial.begin(9600);
  pinMode(US, OUTPUT);
  pinMode(US2, OUTPUT);
  for (int i = FIRST_M; i < FIRST_M + 4; i++) pinMode(i, OUTPUT);
  neck_v.attach(V_SERV);
  h_neck.attach(H_SERV);
  neck_v.write(100);
  h_neck.write(0);
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
      next_box(50);
      move_count += 1;
      delay(300);
      h_neck.write(0);
      delay(300);
      turn(0);
      break;
    case 6:
      h_neck.write(90);
      turn(1);
      delay(300);
      back(move_count, 60);
      move_count = 0;
      break;
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
    case 10:
      Serial.write(get_us(US, US+1));
      Serial.write(get_us(US2,US2+1));
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
  for(byte i=0; i < 5; i++){
    digitalWrite(trig, LOW); //НАЧАЛО ПОЛУЧЕНИЯ ДАННЫХ С US ДАТЧИКА
    delayMicroseconds(5);
    digitalWrite(trig, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig, LOW); //КОНЕЦ ПОЛУЧЕНИЯ ДАННЫХ С US ДАТЧИКА
    int value = pulseIn(echo, HIGH); //НАЧАЛО ОБРАБОТКИ ПОКАЗАНИЙ US
    value = (value / 2) / 29.1;      //КОНЕЦ ОБРАБОТКИ ПОКАЗАНИЙ US
    if (value <= 0) value = 1000;  
    res += value;
    delay(2);
  }
  res = int(res / 5);
  return res;
}



bool next_box(int lim) {
  bool dir = 1;
  while ((get_us(US, US + 1) <= lim) or (get_us(US2, US2 + 1) <= lim)){
    digitalWrite(FIRST_M, !dir);
    digitalWrite(FIRST_M + 1, dir);
    digitalWrite(FIRST_M + 2, dir);
    digitalWrite(FIRST_M + 3, !dir);
//    Serial.write(get_us(US, US + 1));
  }
  stop();
//  Serial.print('a');
  sound(1);
  while (get_us(US, US + 1) > lim or get_us(US2, US2 + 1) > lim) {
    digitalWrite(FIRST_M, !dir);
    digitalWrite(FIRST_M + 1, dir);
    digitalWrite(FIRST_M + 2, dir);
    digitalWrite(FIRST_M + 3, !dir);
//    Serial.write(get_us(US, US + 1));
  }
  delay(200);
  stop();
  sound(1);
  
  //  delay(100);
  return 1;
}

bool back(byte n, byte lim){
  bool dir = 0;
  for (n = n - 1; n > 0; n--){
    while ((get_us(US, US + 1) <= lim) or (get_us(US2, US2 + 1) <= lim)) {
      digitalWrite(FIRST_M, !dir);
      digitalWrite(FIRST_M + 1, dir);
      digitalWrite(FIRST_M + 2, dir);
      digitalWrite(FIRST_M + 3, !dir);
    }
    turn(1);
    stop();
    sound(1);
    while (get_us(US, US + 1) > lim or get_us(US2, US2 + 1) > lim) {
      digitalWrite(FIRST_M, !dir);
      digitalWrite(FIRST_M + 1, dir);
      digitalWrite(FIRST_M + 2, dir);
      digitalWrite(FIRST_M + 3, !dir);
    }
    
    stop();
    sound(1);
    turn(1);
  }
  while ((get_us(US, US + 1) <= lim) or (get_us(US2, US2 + 1) <= lim)) {
      digitalWrite(FIRST_M, !dir);
      digitalWrite(FIRST_M + 1, dir);
      digitalWrite(FIRST_M + 2, dir);
      digitalWrite(FIRST_M + 3, !dir);
  }
  sound(1);
  stop();
  turn(1);
}

bool sound(byte n) {
  for (n; n > 0; n--) {
    tone(11, 300, 500);
    delay(1000);
  }
  return 1;
}

bool turn(bool dir){
  digitalWrite(FIRST_M, !dir);
  digitalWrite(FIRST_M + 1, dir);
  digitalWrite(FIRST_M + 2, !dir);
  digitalWrite(FIRST_M + 3, dir);
  if (dir) while(digitalRead(2)){}
  else while(digitalRead(14)){}
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
  digitalWrite(FIRST_M, 0);
  digitalWrite(FIRST_M + 1, 0);
  digitalWrite(FIRST_M + 2, 0);
  digitalWrite(FIRST_M + 3, 0);
  return;
}
