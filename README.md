# Face Recognition Attendance System (Database Version)

Sistem absensi otomatis menggunakan face recognition berbasis CNN (Convolutional Neural Network) dengan penyimpanan data ke MySQL database.

## Fitur
- Pengambilan data wajah siswa melalui webcam
- Preprocessing data gambar
- Training model CNN untuk pengenalan wajah
- Deteksi wajah secara real-time
- Pencatatan absensi otomatis ke database MySQL
- Export data absensi ke Excel
- View data absensi harian

## Requirements
- Python 3.8+
- MySQL Server
- Webcam

## Setup Database
1. Install MySQL Server
2. Buat user dan password MySQL
3. Edit konfigurasi di `config/database.py`:
   ```python
   DB_HOST = 'localhost'
   DB_USER = 'your_username'
   DB_PASSWORD = 'your_password'
   DB_NAME = 'attendance_system'
   ```
4. Jalankan setup database:
   ```bash
   python setup_database.py
   ```

## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Setup database (lihat section Setup Database)

3. Jalankan program:
   ```bash
   python main_program.py
   ```

## Struktur Database
### Tabel: attendance
- `id` (INT, Primary Key, Auto Increment)
- `student_name` (VARCHAR(100))
- `date` (DATE)
- `time` (VARCHAR(10))
- `status` (VARCHAR(20), default: 'Present')
- `created_at` (DATETIME)

## Menu Program
1. **Collect Student Data** - Kumpulkan foto siswa
2. **Preprocess Data** - Preprocessing gambar
3. **Train Model** - Training model CNN
4. **Run Attendance System** - Jalankan sistem absensi
5. **View Today's Attendance** - Lihat absensi hari ini
6. **Export Attendance to Excel** - Export ke Excel
7. **Exit** - Keluar program

## Branch Information
- `main`: Versi original lastest update
- `excel-version`: Versi dengan Excel (branch ini)
- `db-version`: Versi dengan MySQL database (branch ini)

## Kontributor
- AfrizalAlka

## Lisensi
MIT
