int trigPin = 9;    // Trigger
int echoPin = 11;   // Echo
int buttonPin = 12;
int buttonPin_2 = 13;
int outputPin = 7;   // Define pin 7 as output pin
long duration;
long cm;
unsigned long buttonPressTime = 0;  // To track when button was pressed
boolean outputActive = false;       // Track if output is currently active

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(buttonPin_2, INPUT_PULLUP);
  pinMode(outputPin, OUTPUT);       // Set pin 7 as output
  digitalWrite(outputPin, LOW);     // Ensure it starts LOW
}
 
void loop() {
  int buttonValue = digitalRead(buttonPin);
  int buttonValue_2 = digitalRead(buttonPin_2);
  if (buttonValue == LOW && !outputActive) {
    outputActive = true;
    buttonPressTime = millis();
    digitalWrite(outputPin, HIGH);
  }
  if (outputActive && (millis() - buttonPressTime >= 5000)) {
    outputActive = false;
    digitalWrite(outputPin, LOW);
  }

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
  Serial.print(cm);
  Serial.print(",O:");
  Serial.println(digitalRead(outputPin)); 

  delay(100);
}
