
// библиотека для работы с модулями IMU
#include <TroykaIMU.h>
 
// создаём объект для работы с компасом
Compass compass(COMPASS_ADDRESS_V1);

// если напаяна перемычка, устройство доступно по новому адресу
// Compass compass(COMPASS_ADDRESS_V2);
 
// калибровочные значения, полученные в калибровочной матрице
// из примера compass_cal_matrix
 
const double compassCalibrationBias[3] = {
  -725.096,
  -2117.004,
  3781.861
};
 
const double compassCalibrationMatrix[3][3] = {
  {2.55, 0.099, -1.242},
  {0.075, 1.452, 0.371},
  {0.138, 0.002, 2.213}
};


//void compass_calibration(){
//  for (byte i=0;i < 200;i++){
//    compassCalibrationBias[0] += compass.readX();
//    compassCalibrationBias[1] += compass.readY();
//    compassCalibrationBias[3] += compass.readZ();
//    delay(5);
//  }
//  for(byte j=0;j <3;j++){
//    compassCalibrationBias[j] /= 200;
//  }
//}
 
void setup()
{
  // открываем последовательный порт
  Serial.begin(115200);
  // пока не появились данные с USB
  // выводим сообщение о начале инициализации
  Serial.println("Begin init...");
  // инициализация компаса
  compass.begin();
  // устанавливаем чувствительность компаса
  // ±4 gauss — по умолчанию, ±8 gauss, ±12 gauss, ±16 gauss
  compass.setRange(RANGE_4_GAUSS);
  // калибровка компаса
  compass.calibrateMatrix(compassCalibrationMatrix, compassCalibrationBias);
  // выводим сообщение об удачной инициализации
  Serial.println("Initialization completed");
}
 
void loop()
{
  // выводим азимут относительно оси Z
  Serial.print(compass.readAzimut());
  Serial.println(" Degrees");
  delay(100);
}
