
const int sensorPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int moistureValue = analogRead(sensorPin);

  Serial.print("Soil Moisture: ");
  Serial.println(moistureValue);

  delay(1000);
}
