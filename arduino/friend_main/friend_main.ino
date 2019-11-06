#include <Servo.h>

const byte US = 7, LEFT_H = 9, RIGHT_H = 10;

Servo left_h, right_h;

void setup() {
  Serial.begin(9600);
  pinMode(US, OUTPUT);
  left_h.attach(LEFT_H);
  right_h.attach(RIGHT_H);
}

void loop() {
  if(get_us(US, US + 1) < 20){
    left_h.write(45);
    right_h.write(45);
    delay(1000);
    Serial.write(1);  // ОТПРАВЛЯЕМ СИГНАЛ О ТОМ, ЧТО РУКИ ПОДНЯЛИСЬ
  }

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
