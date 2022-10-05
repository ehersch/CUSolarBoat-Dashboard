// C++ code
//
// we will need to adjust r1 and r2’s values when we create the voltage divider
double r1 = 1.0;
double r2 = 1.0; 

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  double value1 = analogRead(A0);
  double voltage1 = value1 * (5.0/1024.0) *(r1+r2)/r2;
  double value2 = analogRead(A1);
  double voltage2 = value2 * (5.0/1024.0) *(r1+r2)/r2;
  double value3 = analogRead(A2);
  double voltage3 = value3 * (5.0/1024.0) *(r1+r2)/r2;
  
  Serial.println("{V1: " + String(voltage1) + ", V2: " + String(voltage2) + ", V3: " + String(voltage3) + "}");
  delay(1000);
}
