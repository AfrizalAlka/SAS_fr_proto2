import cv2
import os
from datetime import datetime

def collect_student_data(student_name, num_photos=50):
    # Create directory for the student if it doesn't exist
    student_folder = f"data/students/{student_name}"
    if not os.path.exists(student_folder):
        os.makedirs(student_folder)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    count = 0

    print(f"Collecting photos for {student_name}")
    print("Press SPACE to capture photo, ESC to exit")

    while count < num_photos:
        ret, frame = cap.read()
        if not ret:
            break

        # Tampilkan frame
        cv2.putText(frame, f"Photos: {count}/{num_photos}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Student: {student_name}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Data Collection', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE key
            # Simpan foto
            filename = f"{student_folder}/{student_name}_{count:03d}.jpg"
            cv2.imwrite(filename, frame)
            count += 1
            print(f"Saved: {filename}")
            
        elif key == 27:  # ESC key
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()
    print(f"Collected {count} samples for {student_name})")

if __name__ == "__main__":
    student_name = input("Enter student name: ")
    collect_student_data(student_name)