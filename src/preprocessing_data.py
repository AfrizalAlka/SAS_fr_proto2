import os
import pickle
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder

def preprocess_images(data_dir="data/students", img_size=(160, 160)):
    
    # Cek apakah folder data siswa ada
    if not os.path.exists(data_dir):
        print(f"Error: Folder {data_dir} tidak ditemukan!")
        print("Silakan jalankan opsi 1 untuk mengumpulkan data siswa terlebih dahulu.")
        return None, None, None
    
    # Buat folder jika belum ada
    os.makedirs('data/models', exist_ok=True)
    os.makedirs('data/training_data', exist_ok=True)
    
    images = []
    labels = []
    student_names = []

    # Cek apakah ada folder siswa
    student_folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    if not student_folders:
        print(f"Error: Tidak ada folder siswa di {data_dir}!")
        print("Silakan jalankan opsi 1 untuk mengumpulkan data siswa terlebih dahulu.")
        return None, None, None

    for student_name in student_folders:
        student_path = os.path.join(data_dir, student_name)
        if not os.path.isdir(student_path):
            continue

        student_names.append(student_name)
        student_images = 0

        for img_file in os.listdir(student_path):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(student_path, img_file)

                img = cv2.imread(img_path)
                if img is None:
                    print(f"Warning: Tidak bisa membaca {img_path}")
                    continue
                    
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, img_size)
                img = img.astype('float32') / 255.0

                images.append(img)
                labels.append(student_name)
                student_images += 1
        
        print(f"Loaded {student_images} images for {student_name}")
    
    if len(images) == 0:
        print("Error: Tidak ada gambar yang bisa diproses!")
        print("Pastikan folder siswa berisi file gambar (.jpg, .jpeg, .png)")
        return None, None, None

    X = np.array(images)
    y = np.array(labels)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    with open('data/models/label_encoder.pkl', 'wb') as f:
        pickle.dump(label_encoder, f)

    np.save('data/training_data/X_train.npy', X)
    np.save('data/training_data/y_train.npy', y_encoded)

    print(f"Preprocessed {len(X)} images from {len(student_names)} students.")
    print(f"Student names: {list(label_encoder.classes_)}")

    return X, y_encoded, label_encoder

if __name__ == "__main__":
    preprocess_images()
