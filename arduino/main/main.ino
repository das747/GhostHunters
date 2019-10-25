const byte FRST_M = 4, US = 2;
byte com = 0, box = 0;

void setup() {
  Serial.begin(9600);
  pinMode(US, OUTPUT);
  for (int i = FRST_M; i < FRST_M + 4; i++) pinMode(i, OUTPUT);
}

void loop() {
  if (Serial.available()) {  // если пришла команда
    com = Serial.read();  //считываем её
    switch(com){
     case 5:   // команда вперёд
      next_box(40, 1);
      break;
     case 6:  // команда назад
      next_box(40, 0);
      break;
     default: // все остальные команды пищит
      sound(com);
      break;
    }
    Serial.write(1);
  }
}


// получение значения с УЗ датчика
int get_us(int trig, int echo) {
  digitalWrite(trig, LOW); //НАЧАЛО ПОЛУЧЕНИЯ ДАННЫХ С US ДАТЧИКА
  delayMicroseconds(5);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW); //КОНЕЦ ПОЛУЧЕНИЯ ДАННЫХ С US ДАТЧИКА
  int value = pulseIn(echo, HIGH); //НАЧАЛО ОБРАБОТКИ ПОКАЗАНИЙ US
  value = (value / 2) / 29.1; //КОНЕЦ ОБРАБОТКИ ПОКАЗАНИЙ US
  if (value <= 0) value = 0;
  return value;
}


// перемещение к следующей коробке
bool next_box(int lim, bool dir) {
  while (get_us(US, US + 1) <= lim) {  // проезжаем текущую коробку
    digitalWrite(4, !dir);
    digitalWrite(5, dir);
    digitalWrite(6, dir);
    digitalWrite(7, !dir);
  }
  while (get_us(US, US + 1) > lim) {  // доезжаем до следующей
    digitalWrite(4, !dir);
    digitalWrite(5, dir);
    digitalWrite(6, dir);
    digitalWrite(7, !dir);
  }
  digitalWrite(4, 0);  // остановка
  digitalWrite(5, 0);
  digitalWrite(6, 0);
  digitalWrite(7, 0);
  return 1;
}


// пищит заданное кол-во раз
bool sound(byte n) {
  for (n; n > 0; n--) {
    tone(11, 300, 500);
    delay(1000);
  }
}
