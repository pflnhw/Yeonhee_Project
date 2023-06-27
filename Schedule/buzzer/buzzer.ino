char cmd;
int speakerPin = 8;
int numTones = 8;
int tones[] = {262, 294, 330, 349, 392, 440, 494, 523};

void setup() {
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0){
    cmd = Serial.read();
    Serial.println(cmd);
    switch(cmd){
      case '0':
        tone(speakerPin, tones[0], 1000);
        delay(1000);
        noTone(speakerPin);
        delay(1000);
        break;
      case '1':
        tone(speakerPin, tones[1], 1000);
        delay(1000);
        noTone(speakerPin);
        delay(1000);
        break;
      case '2':
        tone(speakerPin, tones[2], 1000);
        delay(1000);
        noTone(speakerPin);
        delay(1000);
        break;
      case '3':
        tone(speakerPin, tones[3], 1000);
        delay(1000);
        noTone(speakerPin);
        delay(1000);
        break;
      case '4':
        tone(speakerPin, tones[4], 1000);
        delay(1000);
        noTone(speakerPin);
        delay(1000);
        break;
      case '5':
        tone(speakerPin, tones[5], 1000);
        delay(1000);
        noTone(speakerPin);
        delay(1000);
        break;
      case '6':
        tone(speakerPin, tones[6], 1000);
        delay(1000);
        noTone(speakerPin);
        delay(1000);
        break;
      case '7':
        tone(speakerPin, tones[7], 1000);
        delay(1000);
        noTone(speakerPin);
        delay(1000);
        break;
    }
    cmd = NULL;
  }
  delay(100);
}
  // for(int i = 0; i < numTones; i++){
  //   tone(speakerPin, tones[i]);
  //   delay(500);
  // }
  // noTone(speakerPin);
  // delay(1000);
