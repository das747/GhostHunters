#include <L3G4200D.h>
#include <Wire.h>

L3G4200D gyro;              //создание гироскопа
float X = 0;                    //переменная для значения с гироскопа
int timeStep=50;  
void setup() {
  pinMode(3, OUTPUT);
  Serial.begin(9600);
  while (!gyro.begin(L3G4200D_SCALE_2000DPS, L3G4200D_DATARATE_400HZ_50)) { // включаем  и калибруем гироскоп
    Serial.println("wait");
    delay(500);
  }
  gyro.calibrate(100);
}
void loop(){
  unsigned long timer=millis();
  Vector norm = gyro.readNormalize();
  bool a = (abs(norm.ZAxis * timeStep / 1000) > 0.05);
  X += norm.ZAxis * timeStep / 1000 * a;
  bool turn = X > 0 and X < 45;
  Serial.println(turn);
  digitalWrite(3, turn);
  delay(timeStep-(millis()-timer));
  
}


