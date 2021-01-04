
//#include <MIDIUSB.h>
             
int THRESHOLD = 150;

void setup() {
 Serial.begin(9600);
}

// // First parameter is the event type (0x09 = note on, 0x08 = note off).
// // Second parameter is note-on/note-off, combined with the channel.
// // Channel can be anything between 0-15. Typically reported to the user as 1-16.
// // Third parameter is the note number (48 = middle C).
// // Fourth parameter is the velocity (64 = normal, 127 = fastest).

// void noteOn(byte channel, byte pitch, byte velocity) {
//   midiEventPacket_t noteOn = {0x09, 0x90 | channel, pitch, velocity};
//   MidiUSB.sendMIDI(noteOn);
// }

// void noteOff(byte channel, byte pitch, byte velocity) {
//   midiEventPacket_t noteOff = {0x08, 0x80 | channel, pitch, velocity};
//   MidiUSB.sendMIDI(noteOff);
// }

byte isTouching(const int piezoPin) {

  byte val = analogRead(piezoPin);


  if(val >= THRESHOLD){
    Serial.print("Choc! - ");
    Serial.print(piezoPin);
    Serial.print(" - ");
    Serial.println(val);
    // noteOn(0, 1, 255);
    // MidiUSB.flush();
    return val;
  }
  return 0;
}


void loop() {
  isTouching(A0);
  isTouching(A1);
  isTouching(A2);
  delay(10);
}

  
