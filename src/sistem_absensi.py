import cv2
import pandas as pd
from datetime import date, datetime
import os
from .face_detection_system import FaceRecognitionSystem
from .models import get_db_session, Attendance, init_database
from sqlalchemy import and_

class AttendanceSystem:
    def __init__(self):
        self.face_system = FaceRecognitionSystem()
        
        # Initialize database
        if not init_database():
            print("Warning: Database initialization failed!")
        
        self.last_recorded = {}
        self.min_interval = 30  # detik (untuk mencegah spam)

    def record_attendance(self, student_name):
        current_time = datetime.now()
        current_date = current_time.date()
        current_time_str = current_time.strftime('%H:%M:%S')

        try:
            # Get database session
            db = get_db_session()
            
            # Cek apakah sudah absen hari ini
            existing_attendance = db.query(Attendance).filter(
                and_(
                    Attendance.student_name == student_name,
                    Attendance.date == current_date
                )
            ).first()
            
            if existing_attendance:
                db.close()
                return False, "Already attended today"
            
            # Cek interval waktu untuk mencegah spam
            if student_name in self.last_recorded:
                time_diff = (current_time - self.last_recorded[student_name]).total_seconds()
                if time_diff < self.min_interval:
                    db.close()
                    return False, "Too soon to record again"
                
            self.last_recorded[student_name] = current_time

            # Simpan ke database
            new_attendance = Attendance(
                student_name=student_name,
                date=current_date,
                time=current_time_str,
                status='Present'
            )
            
            db.add(new_attendance)
            db.commit()
            db.close()
            
            return True, "Attendance recorded successfully"
            
        except Exception as e:
            print(f"Error saving attendance to database: {e}")
            if 'db' in locals():
                db.close()
            return False, "Failed to save attendance"
    
    def get_today_attendance(self):
        """Get today's attendance records"""
        try:
            db = get_db_session()
            today = date.today()
            
            records = db.query(Attendance).filter(Attendance.date == today).all()
            db.close()
            
            return records
        except Exception as e:
            print(f"Error getting attendance records: {e}")
            return []
    
    def get_attendance_by_date(self, target_date):
        """Get attendance records by specific date"""
        try:
            db = get_db_session()
            
            records = db.query(Attendance).filter(Attendance.date == target_date).all()
            db.close()
            
            return records
        except Exception as e:
            print(f"Error getting attendance records: {e}")
            return []
    
    def export_to_excel(self, target_date=None):
        """Export attendance data to Excel file"""
        try:
            db = get_db_session()
            
            if target_date:
                records = db.query(Attendance).filter(Attendance.date == target_date).all()
                filename = f"data/attendance_logs/attendance_{target_date.strftime('%d_%m_%Y')}.xlsx"
            else:
                records = db.query(Attendance).all()
                filename = f"data/attendance_logs/all_attendance_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
            
            db.close()
            
            if not records:
                print("No attendance records found!")
                return False
            
            # Convert to DataFrame
            data = []
            for record in records:
                data.append({
                    'ID': record.id,
                    'Student Name': record.student_name,
                    'Date': record.date.strftime('%d-%m-%Y'),
                    'Time': record.time,
                    'Status': record.status,
                    'Created At': record.created_at.strftime('%d-%m-%Y %H:%M:%S')
                })
            
            df = pd.DataFrame(data)
            
            # Create folder if not exists
            os.makedirs('data/attendance_logs', exist_ok=True)
            
            # Save to Excel
            df.to_excel(filename, index=False)
            print(f"Attendance data exported to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False
        
    def run_attendance_system(self):
        cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture("http://192.168.18.187:8080/video")

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

                    if success:
                        color = (0, 255, 0)
                        status_text = "Recorded"
                    else:
                        if "today" in message:
                            color = (255, 165, 0)  # Orange untuk sudah absen hari ini
                            status_text = "Already Attended Today"
                        else:
                            color = (0, 255, 255)  # Cyan untuk terlalu cepat
                            status_text = "Too Soon"

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
