import os
import sys
from modules.browser import get_driver
from modules.verifKTP import process_ktp
from modules.login import login, close_flyer
# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.utils import log_message, get_last_ktp, save_last_ktp, is_logged_out, backup_log_file
import tkinter as tk
from tkinter import simpledialog
import psutil

def kill_driver_process(driver):
    """Hentikan semua proses WebDriver agar tidak ada koneksi tertinggal."""
    try:
        process = psutil.Process(driver.service.process.pid)
        for child in process.children(recursive=True):
            child.terminate()  # Hentikan semua proses anak
        process.terminate()  # Hentikan proses utama
        log_message("info", "Semua proses WebDriver telah dihentikan.")
    except Exception as e:
        log_message("warning", f"Gagal menghentikan proses WebDriver: {e}")


# === Pilih Mode UI atau Headless ===
print("Pilih Mode:")
print("1. Mode Headless (Tanpa UI)")
print("2. Mode GUI (Dengan UI)")
mode_choice = input("Masukkan pilihan (1/2): ").strip()

# Tentukan apakah menggunakan Headless
use_headless = mode_choice == "1"


# === Pilih Browser ===
browser_options = {
    "1": "chrome",
    "2": "firefox",
    "3": "edge"
}

if use_headless:
    # Jika mode Headless, pilih browser melalui terminal
    print("Pilih browser:")
    print("1. Chrome")
    print("2. Firefox")
    print("3. Edge")
    browser_choice = input("Masukkan pilihan (1/2/3): ").strip()
    #driver = get_driver(browser_choice, use_headless)  # Pass use_headless correctly
    log_message("info", f"Headless mode: {use_headless}")
else:
    # Jika mode GUI, pilih browser melalui simpledialog
    root = tk.Tk()
    root.withdraw()
    browser_choice = simpledialog.askstring(
        "Pilih Browser",
        "Pilih browser untuk menjalankan script:\n1. Chrome\n2. Firefox\n3. Edge",
        parent=root
    )

# Gunakan browser default jika input salah
browser_choice = browser_options.get(browser_choice, "chrome")

# === Inisialisasi WebDriver ===
print(f"Anda memilih: {browser_choice.upper()}, Mode: {'Headless' if use_headless else 'GUI'}")
log_message("info", f"Memulai WebDriver dengan browser {browser_choice.upper()} dalam mode {'Headless' if use_headless else 'GUI'}")
#driver = get_driver(browser_choice, use_headless)

# === Eksekusi Script ===
log_message("info", "WebDriver siap digunakan.")



# Ambil folder tempat script `main.py` berada
script_dir = os.path.dirname(os.path.abspath(__file__))


# Path to the log file and backup file
log_file = os.path.join(script_dir, "log_progres.txt")
backup_file = os.path.join(script_dir, "log_progres_backup.txt")


# If the log file doesn't exist, create an empty one
if not os.path.exists(log_file):
    log_message("info", f"File {log_file} tidak ditemukan. Membuat file kosong...")
    try:
        with open(log_file, "w") as f:
            f.write("")  # Create an empty file
        log_message("info", f"File {log_file} berhasil dibuat.")
    except Exception as e:
        log_message("error", f"Gagal membuat file {log_file}: {e}")

# Fungsi membaca nomor KTP terakhir dari file log
def get_last_ktp(email, log_file):
    """Ambil nomor KTP terakhir dari file txt."""
    try:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                for line in f.readlines():
                    if line.startswith(email + ":"):
                        return line.split(":")[1].strip()
    except Exception as e:
        log_message("error", f"Error membaca progres KTP: {e}")
    return None  # Jika tidak ditemukan, mulai dari awal

# Fungsi menyimpan nomor KTP terakhir
def save_last_ktp(email, last_ktp, log_file):
    """Simpan nomor KTP terakhir ke file txt."""
    try:
        # Baca semua data yang ada
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = f.readlines()
        else:
            lines = []

        # Cari email yang sesuai dan update KTP terakhir
        updated = False
        with open(log_file, "w") as f:
            for line in lines:
                if line.startswith(email + ":"):
                    f.write(f"{email}:{last_ktp}\n")
                    updated = True
                else:
                    f.write(line)
            
            # Jika email tidak ditemukan, tambahkan entri baru
            if not updated:
                f.write(f"{email}:{last_ktp}\n")

        log_message("info", f"Progres KTP terakhir untuk {email} disimpan: {last_ktp}")
    except Exception as e:
        log_message("error", f"Error menyimpan progres KTP: {e}")


# Baca daftar akun dari `akun.txt`
akun_file = os.path.join(script_dir, "akun.txt")

if not os.path.exists(akun_file):
    log_message("error", f"File {akun_file} tidak ditemukan.")
    sys.exit(1)

with open(akun_file, "r") as f:
    akun_list = [line.strip().split(",") for line in f.readlines() if line.strip()]

if not akun_list:
    log_message("error", "Tidak ada akun yang ditemukan di akun.txt.")
    sys.exit(1)

# Backup interval (e.g., every 1 KTPs)
backup_interval = 10

# Loop untuk setiap akun di `akun.txt`
for email, pin in akun_list:
    log_message("info", f"Memproses akun: {email}")

    # Inisialisasi WebDriver baru untuk setiap akun
    driver = get_driver(browser_choice)  

    try:
        login(driver, email, pin)
        log_message("info", f"Login berhasil untuk {email}")
        close_flyer(driver)

        # Path to the KTP file (replace with your actual file path)
        ktp_file = os.path.join(script_dir, f"data_ktp_{email.replace('@', '_').replace('.', '_')}.txt")

        '''
        # Check if the KTP file exists
        if not os.path.exists(ktp_file):
            log_message("error", f"File KTP tidak ditemukan untuk akun {email}: {ktp_file}")
            driver.quit()
            continue
        '''
        
        # If the KTP file doesn't exist, create an empty one
        if not os.path.exists(ktp_file):
            log_message("error", f"File KTP tidak ditemukan untuk akun {email}: {ktp_file}")
            log_message("info", f"Membuat file kosong: {ktp_file}")
            try:
                with open(ktp_file, "w") as f:
                    f.write("")  # Create an empty file
                log_message("info", f"File {ktp_file} berhasil dibuat.")
            except Exception as e:
                log_message("error", f"Gagal membuat file {ktp_file}: {e}")
            continue  # Skip to the next account
        

        # Read KTP numbers from the .txt file
        try:
            with open(ktp_file, "r") as f:
                data_ktp = [line.strip() for line in f.readlines() if line.strip()]
            log_message("info", f"Berhasil membaca file: {ktp_file}")
        except Exception as e:
            log_message("error", f"Terjadi kesalahan saat membaca file: {e}")
            driver.quit()
            continue

        # Process each KTP number
        for idx, ktp in enumerate(data_ktp):
            if is_logged_out(driver):
                log_message("warning", f"{email} terlogout, mencoba login ulang...")
                login(driver, email, pin)

            transaksi_sukses = process_ktp(driver, ktp)

            if transaksi_sukses == "stok_habis":
                log_message("error", f"Stok habis untuk akun {email}. Menghentikan sesi akun ini.")
                driver.quit()  # Tutup WebDriver segera setelah stok habis
                break  # Keluar dari loop KTP, lanjut ke akun berikutnya

            elif transaksi_sukses:
                log_message("info", f"Transaksi berhasil untuk KTP {ktp}")
                save_last_ktp(email, ktp, log_file)  # Simpan progres

                #Back up log file periodically
                if (idx + 1) % backup_interval == 0:
                    backup_log_file(log_file, backup_file)

            else:
                log_message("error", f"Transaksi gagal untuk KTP {ktp}")

    except Exception as e:
        log_message("error", f"Terjadi error pada akun {email}: {e}")

    finally:
        if driver.service.process is not None:
            log_message("info", f"Menutup sesi untuk akun {email}")
            #driver.stop_client()  # Hentikan client Selenium lebih dulu
            #driver.quit()  # Pastikan WebDriver ditutup dengan benar
            #driver.service.stop()  # Pastikan WebDriver mati total
            kill_driver_process(driver)
            #time.sleep(2)


log_message("info", "Semua akun sudah diproses. Program selesai.")
sys.exit(0)
