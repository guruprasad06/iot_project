import serial
import time
from face_verify import verify_face
from student_db import students

# 🔴 Change this to your Arduino COM port
PORT = "COM3"
BAUD_RATE = 9600


def process_uid(uid, ser):
    uid = uid.strip().upper()

    if uid not in students:
        print("Invalid Card ❌")
        ser.write(b"INVALID\n")
        return

    student = students[uid]
    name = student["name"]
    roll = student["roll"]

    print(f"\nCard belongs to: {name} (Roll {roll})")
    print("Starting Face Verification...")

    result = verify_face(name)

    if result:
        print("RESULT: PRESENT ✅")
        ser.write(b"PRESENT\n")
    else:
        print("RESULT: PROXY ❌")
        ser.write(b"PROXY\n")


def main():
    try:
        print("Connecting to Arduino...")
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

        # Wait for Arduino to initialize
        time.sleep(2)

        print("Connected Successfully ✅")
        print("System Ready... Scan Card")

        while True:
            if ser.in_waiting > 0:
                uid = ser.readline().decode(errors='ignore').strip()
                if uid:
                    print("\nReceived UID:", uid)
                    process_uid(uid, ser)

    except serial.SerialException:
        print("❌ Could not open COM port. Check connection.")
    except KeyboardInterrupt:
        print("\nSystem Stopped.")
    finally:
        try:
            ser.close()
        except:
            pass


if __name__ == "__main__":
    main()