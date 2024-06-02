# Menggunakan image Python versi 3.9 sebagai base image
FROM python:3.9

# Mengatur working directory di dalam container
WORKDIR /app

# Menyalin requirements.txt ke dalam container
COPY requirements.txt .

# Menginstal dependencies menggunakan pip
RUN pip install -r requirements.txt

# Menyalin seluruh konten dari direktori aplikasi Anda ke dalam container
COPY . .

# Menjalankan aplikasi Flask ketika container dijalankan
CMD ["python", "main.py"]
