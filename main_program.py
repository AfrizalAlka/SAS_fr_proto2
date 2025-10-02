import sys
import os
from src.face_detection_system import FaceRecognitionSystem
from src.sistem_absensi import AttendanceSystem
from src.create_cnn_model import train_model
from src.preprocessing_data import preprocess_images
from src.data_collection import collect_student_data

def main():
    print("=== Face Recognition Attendance System ===")
    print("1. Collect Student Data")
    print("2. Preprocess Data")
    print("3. Train Model")
    print("4. Run Attendance System")
    print("5. Exit")
    
    while True:
        choice = input("\nChoose option (1-5): ")
        
        if choice == '1':
            student_name = input("Enter student name: ")
            num_photos = int(input("Number of photos to capture (default 50): ") or 50)
            collect_student_data(student_name, num_photos)
            
        elif choice == '2':
            preprocess_images()
            
        elif choice == '3':
            train_model()
            
        elif choice == '4':
            if not os.path.exists('data/models/face_recognition_model.h5'):
                print("Model not found! Please train the model first.")
                continue
            attendance_system = AttendanceSystem()
            attendance_system.run_attendance_system()
            
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please choose 1-5.")

if __name__ == "__main__":
    main()