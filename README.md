# Face Recognition Attendance System

Sistem absensi otomatis menggunakan face recognition berbasis CNN (Convolutional Neural Network).

## Fitur
- Pengambilan data wajah siswa melalui webcam
- Preprocessing data gambar
- Training model CNN untuk pengenalan wajah
- Deteksi wajah secara real-time
- Pencatatan absensi otomatis ke file Excel

## Struktur Folder
```
data/
  students/           # Foto siswa
  training_data/      # Data training (X_train.npy, y_train.npy)
  models/             # Model CNN dan label encoder
  attendance_logs/    # Log absensi (Excel)
src/
  data_collection.py  # Pengambilan data wajah
  preprocessing_data.py# Preprocessing gambar
  create_cnn_model.py # Training model CNN
  face_detection_system.py # Deteksi wajah
  sistem_absensi.py   # Sistem absensi
main_program.py       # Program utama
```

## Cara Penggunaan
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan program utama:
   ```bash
   python main_program.py
   ```
3. Ikuti menu interaktif untuk:
   - Mengumpulkan data siswa
   - Preprocessing data
   - Training model
   - Menjalankan sistem absensi

## Catatan
- Data absensi dan foto siswa tidak di-push ke repository (lihat `.gitignore`).
- Pastikan webcam terhubung dan berfungsi.
- Untuk hasil optimal, gunakan 30-50 foto per siswa dari berbagai sudut.

## Kontributor
- AfrizalAlka

## Lisensi
MIT
