import serial
import time

class Reader:
    def __init__(self, port='COM3', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None

    def connect(self):
        """Ensures the previous connection is closed before opening a new one."""
        try:
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()  

            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(5)  
            print(f"✅ Connected to RFID reader on {self.port}")
        except serial.SerialException as e:
            print(f"❌ Error connecting to RFID reader: {e}")

    def read_card(self):
        """Reads RFID tag data."""
        if not self.serial_conn or not self.serial_conn.is_open:
            print("⚠️ RFID reader not connected.")
            return None

        try:
            while True:
                card_data = self.serial_conn.readline().decode('utf-8').strip()
                if card_data and "RFID Reader Initialized" not in card_data and "Ready to scan" not in card_data:
                    print(f"🎟️ Card detected: {card_data}")
                    return card_data
        except Exception as e:
            print(f"❌ Error reading RFID data: {e}")
            return None

    def close(self):
        """Closes the connection to the RFID reader."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("🔌 RFID reader connection closed.")

# Test standalone
if __name__ == "__main__":
    rfid = Reader(port='COM3')
    rfid.connect()

    try:
        while True:
            tag = rfid.read_card()
            if tag:
                break
            time.sleep(1)
    finally:
        rfid.close()
