#include <Servo.h>

const byte FRST_M = 4, US = 2, V_SERV = 10, H_SERV = 9;
byte com = 0, move_count = 0;

Servo neck_h, neck_v;

void setup() {
  Serial.begin(9600);
  pinMode(US, OUTPUT);
  for (int i = FRST_M; i < FRST_M + 4; i++) pinMode(i, OUTPUT);
  neck_v.attach(V_SERV);
  neck_h.attach(H_SERV);
  neck_v.write(150);
  neck_h.write(90);
}

void loop() {
  if (Serial.available()) {
    com = Serial.read();
    switch (com) {
      case 5:
        Serial.write(next_box(40, 1));
        move_count += 1;
        break;
      case 6:
        for (move_count; move_count > 0; move_count--) next_box(40, 0);
        break;
      default:
        sound(com);
        break;
    }
  }
//    next_box(10, 1);
}

int get_us(int trig, int echo) {
  digitalWrite(trig, LOW); //НАЧАЛО ПОЛУЧЕНИЯ ДАННЫХ С US ДАТЧИКА
  delayMicroseconds(5);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW); //КОНЕЦ ПОЛУЧЕНИЯ ДАННЫХ С US ДАТЧИКА
  int value = pulseIn(echo, HIGH); //НАЧАЛО ОБРАБОТКИ ПОКАЗАНИЙ US
  value = (value / 2) / 29.1;      //КОНЕЦ ОБРАБОТКИ ПОКАЗАНИЙ US
  if (value <= 0) value = 0;
  return value;
}



bool next_box(int lim, bool dir) {
  while (get_us(US, US + 1) <= lim) {
    digitalWrite(4, !dir);
    digitalWrite(5, dir);
    digitalWrite(6, dir);
    digitalWrite(7, !dir);
  }
  while (get_us(US, US + 1) > lim) {
    digitalWrite(4, !dir);
    digitalWrite(5, dir);
    digitalWrite(6, dir);
    digitalWrite(7, !dir);
  }
  digitalWrite(4, 0);
  digitalWrite(5, 0);
  digitalWrite(6, 0);
  digitalWrite(7, 0);
  return 1;
}

bool sound(byte n) {
  for (n; n > 0; n--) {
    tone(11, 300, 500);
    delay(1000);
  }
}
