import cv2
import pandas as pd
from datetime import date, datetime
import os
from .face_detection_system import FaceRecognitionSystem

class AttendanceSystem:
    def __init__(self):
        self.face_system = FaceRecognitionSystem()
        self.attendance_file = f"data/attendance_logs/attendance_{date.today().strftime('%d_%m_%Y')}.xlsx"
        self.last_recorded = {}
        self.min_interval = 1  # menit

    def record_attendance(self, student_name):
        current_time = datetime.now()

        if student_name in self.last_recorded:
            time_diff = (current_time - self.last_recorded[student_name]).total_seconds()
            if time_diff < self.min_interval:
                return False, "Already recorded recently"
            
        self.last_recorded[student_name] = current_time

        attendance_data = {
            'Student Name': student_name,
            'Date': current_time.strftime('%d-%m-%Y'),
            'Time': current_time.strftime('%H:%M:%S'),
            'Status': 'Present'
        }

        if os.path.exists(self.attendance_file):
            df = pd.read_excel(self.attendance_file)
            df = pd.concat([df, pd.DataFrame([attendance_data])], ignore_index=True)
        else:
            df = pd.DataFrame([attendance_data])

        df.to_excel(self.attendance_file, index=False)
        return True, "Attendance recorded successfully"
        
    def run_attendance_system(self):
        cap = cv2.VideoCapture(0)

        print("Starting attendance system. Press 'q' to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            faces = self.face_system.detect_faces(frame)

            for (x, y, w, h) in faces:
                face_roi = frame[y:y+h, x:x+w]
                face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)

                name, confidence = self.face_system.predict_face(face_rgb)

                if name != "Unknown":

                    success, message = self.record_attendance(name)

                    color = (0, 255, 0) if success else (0, 255, 255)
                    status_text = "Recorded" if success else "Already Recorded"

                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, f"{name} - {status_text}",
                                (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    
                    if success:
                        print(f"{name} attendance recorded at {datetime.now().strftime('%H:%M:%S')}")
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(frame, "Unknown",
                                (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
            cv2.putText(frame, f"Date: {date.today().strftime('%d-%m-%Y')}", (10, 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Time: {datetime.now().strftime('%H:%M:%S')}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Attendance System', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    attendance_system = AttendanceSystem()
    attendance_system.run_attendance_system()
