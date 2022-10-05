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
  
  Serial.print("Voltage 1: ");
  Serial.println(voltage1);
  delay(5000);
}





