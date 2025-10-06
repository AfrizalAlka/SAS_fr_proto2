import sys
import os
from datetime import date
from src.face_detection_system import FaceRecognitionSystem
from src.sistem_absensi import AttendanceSystem
from src.create_cnn_model import train_model
from src.preprocessing_data import preprocess_images
from src.data_collection import collect_student_data

def main():
    print("=== Face Recognition Attendance System (Database Version) ===")
    print("1. Collect Student Data")
    print("2. Preprocess Data")
    print("3. Train Model")
    print("4. Run Attendance System")
    print("5. View Today's Attendance")
    print("6. Export Attendance to Excel")
    print("7. View Attendance Photo")
    print("8. Save Photo to File")
    print("9. Exit")
    
    while True:
        choice = input("\nChoose option (1-9): ")
        
        if choice == '1':
            student_name = input("Enter student name: ")
            num_photos = int(input("Number of photos to capture (default 50): ") or 50)
            collect_student_data(student_name, num_photos)
            
        elif choice == '2':
            result = preprocess_images()
            if result[0] is None:
                print("Preprocessing gagal. Silakan periksa data siswa.")
                continue
            
        elif choice == '3':
            result = train_model()
            if result[0] is None:
                print("Training gagal. Silakan periksa data preprocessing.")
                continue
            
        elif choice == '4':
            if not os.path.exists('data/models/face_recognition_model.h5'):
                print("Model not found! Please train the model first.")
                continue
            attendance_system = AttendanceSystem()
            attendance_system.run_attendance_system()
            
        elif choice == '5':
            # View today's attendance
            attendance_system = AttendanceSystem()
            records = attendance_system.get_today_attendance()
            
            if not records:
                print("No attendance records for today.")
            else:
                print(f"\n=== Today's Attendance ({date.today().strftime('%d-%m-%Y')}) ===")
                for record in records:
                    photo_status = "📷 Yes" if record.photo_data else "❌ No"
                    confidence = f" (Confidence: {record.confidence_score})" if record.confidence_score else ""
                    print(f"ID: {record.id} | Name: {record.student_name} | Time: {record.time} | Status: {record.status} | Photo: {photo_status}{confidence}")
            
        elif choice == '6':
            # Export to Excel
            attendance_system = AttendanceSystem()
            export_choice = input("Export (1) Today only or (2) All records? Enter 1 or 2: ")
            
            if export_choice == '1':
                result = attendance_system.export_to_excel(date.today())
            else:
                result = attendance_system.export_to_excel()
            
            if result:
                print("Export successful!")
            else:
                print("Export failed!")
            
        elif choice == '7':
            # View attendance photo
            attendance_system = AttendanceSystem()
            
            try:
                attendance_id = int(input("Enter attendance ID to view photo: "))
                photo_data, filename = attendance_system.get_attendance_photo(attendance_id)
                
                if photo_data:
                    print(f"Photo found: {filename}")
                    
                    # Convert binary data back to image and display
                    import numpy as np
                    import cv2
                    
                    # Convert binary to numpy array
                    nparr = np.frombuffer(photo_data, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    
                    if img is not None:
                        # Resize image for better display
                        height, width = img.shape[:2]
                        if width > 800:
                            scale = 800 / width
                            new_width = 800
                            new_height = int(height * scale)
                            img = cv2.resize(img, (new_width, new_height))
                        
                        cv2.imshow(f'Attendance Photo - ID: {attendance_id}', img)
                        print("Press any key to close the photo...")
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                    else:
                        print("Error: Could not decode image data.")
                else:
                    print("No photo found for this attendance ID.")
                    
            except ValueError:
                print("Invalid attendance ID. Please enter a number.")
            except Exception as e:
                print(f"Error viewing photo: {e}")
        
        elif choice == '8':
            # Save photo to file
            attendance_system = AttendanceSystem()
            
            try:
                attendance_id = int(input("Enter attendance ID to save photo: "))
                output_path = input("Enter output path (press Enter for default): ").strip()
                
                if not output_path:
                    output_path = None
                
                if attendance_system.save_photo_to_file(attendance_id, output_path):
                    print("Photo saved successfully!")
                else:
                    print("Failed to save photo.")
                    
            except ValueError:
                print("Invalid attendance ID. Please enter a number.")
            except Exception as e:
                print(f"Error saving photo: {e}")
            
        elif choice == '9':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please choose 1-9.")

if __name__ == "__main__":
    main()