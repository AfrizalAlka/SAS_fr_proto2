import os
import pickle
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder

def preprocess_images(data_dir="data/student", img_size=(160, 160)):
    
    images = []
    labels = []
    student_names = []

    for student_name in os.listdir(data_dir):
        student_path = os.path.join(data_dir, student_name)
        if not os.path.isdir(student_path):
            continue

        student_names.append(student_name)

        for img_file in os.listdir(student_path):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(student_path, img_file)

                img = cv2.imread(img_path)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, img_size)
                img = img.astype('float32') / 255.0

                images.append(img)
                labels.append(student_name)

    X = np.array(images)
    y = np.array(labels)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    with open('data/models/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)

    np.save('data/training_data/X_train.npy', X)
    np.save('data/training_data/y_train.npy', y_encoded)

    print(f"Preprocessed {len(X)} images from {len(student_names)} student.")
    print(f"Student names: {list(label_encoder.classes_)}")

    return X, y_encoded, label_encoder

if __name__ == "__main__":
    preprocess_images()
