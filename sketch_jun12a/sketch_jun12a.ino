//Sihab Sahariar- 12-06-2021
int data1=0;
void setup() {
  Serial.begin(9600);
}

void loop() {
  data1 =data1+random(10);
  Serial.println(data1);
  delay(1000);
}
