#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define BUZZER 6    // Buzzer pin
#define GREEN_LED 7 // Green LED pin
#define RED_LED 8   // Red LED pin

MFRC522 rfid(SS_PIN, RST_PIN);
String tagID = "";

// List of valid RFID tags (hex format, lowercase)
String validTags[] = {"abcd1234", "11223344", "deadbeef"};  

void setup() {
    Serial.begin(9600);
    SPI.begin();
    rfid.PCD_Init();

    pinMode(BUZZER, OUTPUT);
    pinMode(GREEN_LED, OUTPUT);
    pinMode(RED_LED, OUTPUT);

    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, LOW);

    Serial.println("RFID Reader Initialized...");
}

void loop() {
    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        return;
    }

    tagID = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        tagID += String(rfid.uid.uidByte[i], HEX); // Convert tag to hex string
    }

    Serial.println(tagID);  // Send RFID data to Python

    // Check if RFID is valid
    bool isValid = false;
    for (String validTag : validTags) {
        if (tagID == validTag) {
            isValid = true;
            break;
        }
    }

    if (isValid) {
        successFeedback();
    } else {
        failureFeedback();
    }

    rfid.PICC_HaltA();
}

// Function to indicate successful scan
void successFeedback() {
    digitalWrite(GREEN_LED, HIGH);
    digitalWrite(RED_LED, LOW);
    tone(BUZZER, 1000, 200);  // Short beep
    delay(500);
    digitalWrite(GREEN_LED, LOW);
}

// Function to indicate failed scan
void failureFeedback() {
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, HIGH);
    tone(BUZZER, 500, 500);  // Longer beep
    delay(500);
    digitalWrite(RED_LED, LOW);
}
