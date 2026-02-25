from deepface import DeepFace
import cv2
import os
import time


def verify_face(expected_name):

    cap = cv2.VideoCapture(0)
    print("Look at camera...")
    print("Auto capturing...")

    match_count = 0
    attempts = 3

    for i in range(attempts):

        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Face Verification", frame)
        cv2.waitKey(800)  # Small delay between captures

        temp_file = f"temp_{i}.jpg"
        cv2.imwrite(temp_file, frame)

        try:
            results = DeepFace.find(
                img_path=temp_file,
                db_path="faces",
                enforce_detection=False,
                detector_backend="opencv",
                silent=True
            )

            if len(results) > 0 and not results[0].empty:
                identity_path = results[0].iloc[0]["identity"]
                detected_name = os.path.basename(os.path.dirname(identity_path))

                print("Detected:", detected_name)

                if detected_name.lower() == expected_name.lower():
                    match_count += 1

        except:
            pass

        time.sleep(0.5)

    cap.release()
    cv2.destroyAllWindows()

    # Clean temp files
    for i in range(attempts):
        if os.path.exists(f"temp_{i}.jpg"):
            os.remove(f"temp_{i}.jpg")

    # 2 out of 3 rule
    if match_count >= 2:
        print("Face Matched ✅")
        return True
    else:
        print("Proxy Detected ❌")
        return False