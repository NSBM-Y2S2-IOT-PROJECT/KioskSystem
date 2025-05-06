int trigPin = 9;    // Trigger
int echoPin = 11;   // Echo
int buttonPin = 12;
int buttonPin_2 = 13;
long duration;
long cm;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buttonPin_2, INPUT_PULLUP);
}
 
void loop() {
  // Read buttons
  int buttonValue = digitalRead(buttonPin);
  int buttonValue_2 = digitalRead(buttonPin_2);

  // Measure distance
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH, 30000); // timeout after 30ms
  if (duration == 0) {
    cm = -1; // No echo
  } else {
    cm = (duration / 2) / 29.1;
  }

  // Output a single line of data
  Serial.print("B1:");
  Serial.print(buttonValue);
  Serial.print(",B2:");
  Serial.print(buttonValue_2);
  Serial.print(",D:");
  Serial.println(cm);  // 'cm' is the distance

  delay(100); // 100ms delay (~10 readings per second)
}
