
#include <MIDIUSB.h>
             
int THRESHOLD = 200;

const int n_sensors = 3;
int    sensorPins[n_sensors] = {A0, A1, A2};
int    sensorNotes[n_sensors] = {48, 49, 50};
double sensorVals[n_sensors] = {millis(), millis(), millis()};
double sensorTimeToNoteOff[n_sensors] = {millis(), millis(), millis()};
int sensorStatus[n_sensors] = {0, 0, 0};
bool noteIsOn[n_sensors] = {false, false, false};
bool noteHasToBeOff[n_sensors] = {false, false, false};
double t_last_note[n_sensors];

int t_between_notes = 100; // Min. time until next trigger from sensor (ms)
int note_duration = 100;  // Time until note is cut off (ms)
double threshold = 130; // Sensors must cross this level to be registered as a note
int waves = 4; // number of times threshold had to be crossed

void setup() {
 delay(1000);
 Serial.begin(9600);
}

// // First parameter is the event type (0x09 = note on, 0x08 = note off).
// // Second parameter is note-on/note-off, combined with the channel.
// // Channel can be anything between 0-15. Typically reported to the user as 1-16.
// // Third parameter is the note number (48 = middle C).
// // Fourth parameter is the velocity (64 = normal, 127 = fastest).

void noteOn(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOn = {0x09, 0x90 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOn);
  MidiUSB.flush();
}

void noteOff(byte channel, byte pitch, byte velocity) {
  midiEventPacket_t noteOff = {0x08, 0x80 | channel, pitch, velocity};
  MidiUSB.sendMIDI(noteOff);
  MidiUSB.flush();
}

void isTouching(int sensorId) {

  double val = analogRead(sensorPins[sensorId]);

  if(noteIsOn[sensorId] == true && millis() - t_last_note[sensorId] > t_between_notes) {
    Serial.println("ready");
    noteIsOn[sensorId] = false;
  }
  if(noteHasToBeOff[sensorId] == true && millis() - sensorTimeToNoteOff[sensorId] > note_duration) {
    noteOff(0, sensorNotes[sensorId], 0);
    noteHasToBeOff[sensorId] = false;
  }
  // if we trigger a value modification that is bigger than the threshold value
  if (noteIsOn[sensorId] == false && abs(val - sensorVals[sensorId]) > threshold) {       
    t_last_note[sensorId] = millis();
    sensorVals[sensorId] = val;
    sensorStatus[sensorId]++;
  }
  // if we trigger touch 
  if(sensorStatus[sensorId] >= waves) {
    noteIsOn[sensorId] = true;
    sensorStatus[sensorId] = 0;
    sensorTimeToNoteOff[sensorId] = millis();
    noteHasToBeOff[sensorId] = true;
    Serial.print("Choc! -> ");
    Serial.println(sensorId);
    noteOn(0, sensorNotes[sensorId], 127);
  }

}

void loop() {
  isTouching(0);
  isTouching(1);
  isTouching(2);
  delay(1);
}

  
