import os
import logging
import shutil
import time
from datetime import datetime
import pytz
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#FUNGSI LOGGING
# Zona waktu UTC+7
from datetime import datetime
import pytz

def get_current_time_utc7():
    """Get the current date and time in UTC+7 (Asia/Jakarta)."""
    utc7 = pytz.timezone("Asia/Jakarta")
    return datetime.now(utc7).strftime("%Y-%m-%d - %H:%M")

timezone = pytz.timezone("Asia/Jakarta")

# Buat folder logs jika belum ada
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Tentukan format nama file log: YYYYMMDD_HHMM.txt
current_time = datetime.now(timezone).strftime("%Y%m%d_%H%M")
log_filename = os.path.join(LOG_DIR, f"{current_time}.txt")

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename, mode="a"),
        logging.StreamHandler(sys.stdout)  # Outputkan ke terminal juga
    ],
    force=True  # Pastikan log langsung ditulis tanpa buffering
)

# Paksa output agar langsung ditulis ke file dan terminal tanpa delay
sys.stdout.reconfigure(line_buffering=True)


# Fungsi untuk mencatat log
def log_message(level, message):
    """Mencatat pesan ke log dengan level tertentu."""
    timestamp = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {level.upper()} - {message}"

    if level.lower() == "info":
        logging.info(message)
    elif level.lower() == "warning":
        logging.warning(message)
    elif level.lower() == "error":
        logging.error(message)
    elif level.lower() == "debug":
        logging.debug(message)
    else:
        logging.info(message)
    
    '''
    # Paksa output langsung muncul
    sys.stdout.flush()
    sys.stderr.flush()
    '''

# Fungsi membaca nomor KTP terakhir dari log_progres.txt
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

# Fungsi menyimpan nomor KTP terakhir yang berhasil diproses
def save_last_ktp(email, last_ktp, log_file):
    """Simpan nomor KTP terakhir ke file txt dengan backup real-time."""
    try:
        # Path to the temporary file
        temp_file = log_file + ".temp"

        # Get the current time in UTC+7
        timestamp = get_current_time_utc7()

        # Baca semua data yang ada
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                lines = f.readlines()
        else:
            lines = []

        # Cari email yang sesuai dan update KTP terakhir
        updated = False
        with open(temp_file, "w") as f:
            for line in lines:
                if line.split(":")[-2] == email:  # Check the email part of the line
                    f.write(f"{timestamp}:{email}:{last_ktp}\n")  # Update with new timestamp
                    updated = True
                else:
                    f.write(line)
            
            # Jika email tidak ditemukan, tambahkan entri baru
            if not updated:
                f.write(f"{timestamp}:{email}:{last_ktp}\n")

        # Atomically replace the main file with the temporary file
        os.replace(temp_file, log_file)

        log_message("info", f"Progres KTP terakhir untuk {email} disimpan: {last_ktp}")
    except Exception as e:
        log_message("error", f"Error menyimpan progres KTP: {e}")

# FUNGSI BACKUP LOG_PROGRESS.TXT SECARA BERKALA
def backup_log_file(log_file, backup_file):
    """Backup log file to a backup file."""
    try:
        if os.path.exists(log_file):
            shutil.copy(log_file, backup_file)
            log_message("info", f"Backup log file berhasil dibuat: {backup_file}")
    except Exception as e:
        log_message("error", f"Gagal membuat backup log file: {e}")


# FUNGSI CEK LOGOUT
def is_logged_out(driver):
    """Cek apakah user sudah logout sebelum melakukan aksi lain."""
    if driver.session_id is None:  # Jika WebDriver sudah ditutup, hentikan
        return True
    try:
        return "auth/login" in driver.current_url or \
               WebDriverWait(driver, 3).until(
                   EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email atau No. Handphone']"))
               )
    except:
        return False





'''
# Fungsi Menyimpan Akun ke File
import os

ACCOUNTS_FILE = "accounts.txt"

def save_account(email, pin):
    """Simpan akun ke dalam file jika belum ada."""
    if not os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "w") as f:
            f.write("")  # Buat file kosong jika belum ada

    # Cek apakah akun sudah tersimpan
    with open(ACCOUNTS_FILE, "r") as f:
        accounts = f.readlines()

    for acc in accounts:
        saved_email, _ = acc.strip().split("|")
        if saved_email == email:
            return  # Jangan simpan akun duplikat

    # Simpan akun baru
    with open(ACCOUNTS_FILE, "a") as f:
        f.write(f"{email}|{pin}\n")

def load_accounts():
    """Muat daftar akun dari file."""
    if not os.path.exists(ACCOUNTS_FILE):
        return []

    with open(ACCOUNTS_FILE, "r") as f:
        accounts = [line.strip().split("|") for line in f.readlines()]

    return accounts  # Format: [('email1', 'pin1'), ('email2', 'pin2')]
'''