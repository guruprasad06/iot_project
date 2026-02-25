from deepface import DeepFace
import cv2
import os

# Path to face database
db_path = "faces"

# Open webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Save frame temporarily
        temp_image_path = "temp.jpg"
        cv2.imwrite(temp_image_path, frame)

        # Search for matching face
        results = DeepFace.find(
            img_path=temp_image_path,
            db_path=db_path,
            enforce_detection=False,
            detector_backend="opencv",
            silent=True
        )

        name = "Unknown"

        # Check if match found
        if len(results) > 0 and not results[0].empty:
            identity_path = results[0].iloc[0]["identity"]

            # Extract folder name (person name)
            name = os.path.basename(os.path.dirname(identity_path))

        # Display name on screen
        cv2.putText(
            frame,
            f"Match: {name}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    except Exception:
        pass

    cv2.imshow("Face Recognition", frame)

    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()