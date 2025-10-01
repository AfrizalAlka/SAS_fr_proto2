import cv2
import numpy as np
import tensorflow as tf
import pickle
from datetime import datetime

class FaceRecognitionSystem:
    def __init__(self):
        self.model = tf.keras.models.load_model('data/models/face_recognition_model.h5')

        with open('data/models/label_encoder.pkl', 'rb') as f:
            self.label_encoder = pickle.load(f)
        
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        self.img_size = (128, 128)
        self.confidence_threshold = 0.7
    
    def preprocess_face(self, face_img):
        face_img = cv2.resize(face_img, self.img_size)
        face_img = face_img.astype('float32') / 255.0
        face_img = np.expand_dims(face_img, axis=0)
        return face_img
    
    def predict_face(self, face_img):
        processed_face = self.preprocess_face(face_img)
        predictions = self.model.predict(processed_face, verbose=0)
        
        confidence = np.max(predictions)
        predicted_class = np.argmax(predictions)
        
        if confidence > self.confidence_threshold:
            student_name = self.label_encoder.inverse_transform([predicted_class])[0]
            return student_name, confidence
        else:
            return "Unknown", confidence
    
    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces

if __name__ == "__main__":
    system = FaceRecognitionSystem()
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        faces = system.detect_faces(frame)
        
        for (x, y, w, h) in faces:
            # Extract face
            face_roi = frame[y:y+h, x:x+w]
            face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
            
            name, confidence = system.predict_face(face_rgb)
            
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{name} ({confidence:.2f})", 
                       (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        cv2.imshow('Face Recognition Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()