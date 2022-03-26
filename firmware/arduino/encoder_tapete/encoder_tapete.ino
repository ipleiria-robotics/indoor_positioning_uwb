int val;
int encoder0PinA = 2; //GPIO pin 2
int encoder0PinB = 4; //GPIO pin 4
int encoder0Pos = -1;
int encoder0PinALast = LOW;
int encoder0PinBLast = LOW;
int n = 0;
int firstTime = 0;


void setup() {
  pinMode (encoder0PinA, INPUT_PULLUP);
  pinMode (encoder0PinB, INPUT_PULLUP);
  Serial.begin (115200);
  delay(200);
  int encoder0Pos = 1;
  Serial.print("Start\n");
}

void loop() {
  
  n = digitalRead(encoder0PinA);
  
  delay(3);
 
  if ((encoder0PinALast == LOW) && (n == HIGH)) {
    if (digitalRead(encoder0PinB) == LOW) {
      encoder0Pos++;
    } else {
      encoder0Pos--;
    }
    Serial.print(encoder0Pos);
    Serial.print("\n");
  }
  encoder0PinALast = n;
}
