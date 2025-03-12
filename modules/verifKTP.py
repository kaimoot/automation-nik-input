from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .utils import log_message

# Fungsi untuk mengecek apakah stok tabung kosong
def check_stock_empty(driver):
    try:
        # Cek apakah pesan stok habis ada di halaman setelah cek KTP
        stock_message = driver.find_element(By.XPATH, "//*[contains(text(), 'stok tabung yang dapat dijual kosong')]")
        if stock_message:
            log_message("error", "Stok tabung kosong. Menghentikan sesi akun ini.")
            return "stok_habis" # Kembalikan info ke main.py agar bisa menangani sesi dengan benar
    except:
        pass
    return "stok_tersedia"  # Jika tidak ada pesan stok habis

# Fungsi untuk mengisi dan memproses data KTP
def process_ktp(driver, ktp):
    """Proses verifikasi dan transaksi KTP."""
    if driver.session_id is None:  # Cek apakah driver masih aktif
        log_message("error", "Driver sudah ditutup. Menghentikan proses KTP.")
        return False  

    try:
        driver.get('https://subsiditepatlpg.mypertamina.id/merchant/app/verification-nik')

        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Masukkan 16 digit NIK KTP Pelanggan"]'))
        )
        input_field.clear()
        input_field.send_keys(ktp)

        check_button = driver.find_element(By.XPATH, "//button[text()='Cek']")
        check_button.click()
        
        # Tunggu hasilnya muncul
        time.sleep(6)  # Sesuaikan waktu tunggu dengan kecepatan situs web
        
       # Cek apakah stok kosong
        if check_stock_empty(driver) == "stok_habis":
            return "stok_habis"
        
        # Cek apakah nomor KTP terdaftar atau tidak
        page_source = driver.page_source

        if "NIK belum terdaftar" in page_source or "NIK tidak valid karena di bawah 17 tahun" in page_source:
            log_message("info", f"KTP {ktp} tidak terdaftar")
            return False

        elif "Pilih salah satu jenis pengguna untuk melanjutkan transaksi" in page_source:
            # Tunggu dan pilih opsi di pop-up jika ada 2 jenis pengguna
            time.sleep(2)

            # Cek apakah ada dua jenis pengguna Rumah Tangga dan Usaha Mikro
            try:
                um_radio_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "styles_radioButton__zTm99"))  # Radio button Usaha Mikro
                )
                um_radio_button.click()  # Pilih Usaha Mikro

                # Klik tombol "Lanjut Transaksi" setelah memilih jenis pengguna
                lanjut_transaksi_button = driver.find_element(By.XPATH, "//button[text()='Lanjut Transaksi']")
                lanjut_transaksi_button.click()
                time.sleep(5)  # Tunggu halaman berikutnya terbuka
                
                # Setelah melanjutkan transaksi, isi jumlah tabung untuk Usaha Mikro
                tabung_value = 1  # Isi 3 tabung untuk Usaha Mikro

            except Exception as e:
                log_message("error", f"Error selecting 'Usaha Mikro', trying 'Rumah Tangga' and 'Pengecer': {e}")

                # Jika ditemukan Rumah Tangga dan Pengecer, pilih Rumah Tangga
                try:
                    rt_radio_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "styles_radioButton__zTm99"))  # Radio button Rumah Tangga
                    )
                    rt_radio_button.click()  # Pilih Rumah Tangga

                    # Klik tombol "Lanjut Transaksi" setelah memilih jenis pengguna
                    lanjut_transaksi_button = driver.find_element(By.XPATH, "//button[text()='Lanjut Transaksi']")
                    lanjut_transaksi_button.click()
                    time.sleep(5)  # Tunggu halaman berikutnya terbuka
                    
                    # Setelah melanjutkan transaksi, isi jumlah tabung untuk Rumah Tangga
                    tabung_value = 1  # Isi 1 tabung untuk Rumah Tangga

                except Exception as e:
                    log_message("error", f"Error selecting 'Rumah Tangga' and 'Pengecer': {e}")
                    return False
            
        elif "Rumah Tangga" in page_source:
            # Jika terdaftar sebagai Rumah Tangga
            tabung_value = 1  # 1 tabung untuk Rumah Tangga
        elif "Usaha Mikro" in page_source:
            # Jika terdaftar sebagai Usaha Mikro
            tabung_value = 3  # 3 tabung untuk Usaha Mikro
        else:
            log_message("info", f"KTP {ktp} terdaftar, tetapi tidak ditemukan jenis pengguna yang valid")
            return False

        # Jika status terdaftar, lanjutkan dengan input tabung dan proses transaksi
        if tabung_value:
            # Menggunakan tombol "+" berdasarkan class yang diberikan "icon icon-tabler icon-tabler-plus"
            plus_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "icon-tabler-plus"))
            )

            # Klik tombol "+" sesuai jumlah tabung yang diperlukan
            for _ in range(tabung_value - 0):  # Mulai dari 1 tabung, jadi klik untuk tambah sisanya
                plus_button.click()
                time.sleep(1)  # Beri jeda waktu kecil setelah setiap klik
            
            # Klik tombol Cek Pesanan berdasarkan teks "Cek Pesanan"
            cek_pesanan_button = driver.find_element(By.XPATH, "//button[text()='Cek Pesanan']")
            cek_pesanan_button.click()
            
            # Tunggu halaman konfirmasi pesanan
            time.sleep(5)
            
            # Klik tombol Proses Transaksi berdasarkan teks "Proses Transaksi"
            proses_transaksi_button = driver.find_element(By.XPATH, "//button[text()='Proses Transaksi']")
            proses_transaksi_button.click()

            log_message("info", f"Proses transaksi berhasil untuk KTP {ktp} dengan {tabung_value} tabung")
            #sys.stdout.flush()
            return True

    except Exception as e:
        log_message("error", f"Error processing KTP {ktp}: {e}")
        return False
    