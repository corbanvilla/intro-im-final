#include <Arduino.h>
#include <stdint.h>

// Enable human-readable debug output to serial
#define DEBUG false

// Print/send interval in ms
const unsigned long PRINT_INTERVAL = 1000;
const unsigned long PRINT_COOLOFF = 250;

// Track last print time
unsigned long lastPrintTime = 0;

struct Control {
    uint8_t pot1;
    uint8_t pot2;
    uint8_t pot3;
    bool button1;
    bool button2;
    bool switch1;
};

Control ctrl;

void setup() {
    Serial.begin(9600);

    ctrl.pot1 = 0;
    ctrl.pot2 = 0;
    ctrl.pot3 = 0;
    ctrl.button1 = false;
    ctrl.button2 = false;
    ctrl.switch1 = false;

    pinMode(2, INPUT_PULLUP);
    pinMode(3, INPUT_PULLUP);
    pinMode(4, INPUT);
}

void loop() {
    bool stateChanged = false;

    // --- All sensor reads at the top ---
    int analogValue = analogRead(A0);
    // Adjust A0: subtract 230, clamp to 0-25, then map to 0-255
    int adjustedValue = analogValue - 230;
    if (adjustedValue < 0) adjustedValue = 0;
    if (adjustedValue > 25) adjustedValue = 25;
    uint8_t mappedValue = map(adjustedValue, 0, 25, 0, 255);

    int analogValue1 = analogRead(A1);
    uint8_t mappedValue1 = map(analogValue1, 0, 1023, 0, 255);

    int analogValue2 = analogRead(A2);
    uint8_t mappedValue2 = map(analogValue2, 0, 1023, 0, 255);

    bool switch1State = digitalRead(4);
    bool buttonState = digitalRead(2);
    bool buttonState2 = digitalRead(3);
    // --- End sensor reads ---

    ctrl.switch1 = switch1State;

    // If value changed, update and set stateChanged
    if (ctrl.pot1 != mappedValue) {
        ctrl.pot1 = mappedValue;
        stateChanged = true;
    }

    if (ctrl.pot2 != mappedValue1) {
        ctrl.pot2 = mappedValue1;
        stateChanged = true;
    }

    if (ctrl.pot3 != mappedValue2) {
        ctrl.pot3 = mappedValue2;
        stateChanged = true;
    }

    // Button handling on pin 2 (active low)
    static bool lastButtonState = HIGH;

    if (buttonState != lastButtonState) {
        lastButtonState = buttonState;
        if (buttonState == LOW) {
            ctrl.button1 = true;
        } else {
            ctrl.button1 = false;
        }
        stateChanged = true;
    }

    // Button handling on pin 3 (active low)
    static bool lastButtonState2 = HIGH;

    if (buttonState2 != lastButtonState2) {
        lastButtonState2 = buttonState2;
        if (buttonState2 == LOW) {
            ctrl.button2 = true;
        } else {
            ctrl.button2 = false;
        }
        stateChanged = true;
    }

    // Print debug info
    unsigned long now = millis();
    if (DEBUG) {
        Serial.print(ctrl.pot1);
        Serial.print(",");
        Serial.print(ctrl.pot2);
        Serial.print(",");
        Serial.print(ctrl.pot3);
        Serial.print(",");
        Serial.print(ctrl.button1 ? "PRESSED" : "RELEASED");
        Serial.print(",");
        Serial.print(ctrl.button2 ? "PRESSED" : "RELEASED");
        Serial.print(",");
        Serial.println(ctrl.switch1 ? "ON" : "OFF");
        delay(PRINT_INTERVAL);
    } else if (stateChanged || (now - lastPrintTime > PRINT_INTERVAL)) {
        Serial.write((uint8_t*)&ctrl, sizeof(ctrl));
        lastPrintTime = now;
        delay(PRINT_COOLOFF);
    }
}