void setup(){
    Serial.begin(9600);
}

void loop()
{
    int d = Serial.read();
    Serial.println(d,BYTE);
}