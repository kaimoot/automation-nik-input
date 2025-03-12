from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .utils import log_message

# Fungsi untuk login
def login(driver, email, pin):
    """Log in to the website using the provided email and PIN."""
    driver.get('https://subsiditepatlpg.mypertamina.id/merchant/auth/login')

    # Tunggu hingga elemen input email tersedia
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email atau No. Handphone']"))
    )
    email_input.clear()
    email_input.send_keys(email)

    # Tunggu hingga elemen input PIN tersedia
    pin_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='PIN (6-digit)']"))
    )
    pin_input.clear()
    pin_input.send_keys(pin)

    # Klik tombol login menggunakan XPATH berdasarkan teks tombol
    try:
        submit_button = driver.find_element(By.XPATH, "//button[text()='Masuk']")
        submit_button.click()
        log_message("info", "Tombol 'Masuk' ditemukan dan berhasil diklik.")
        # Tunggu hingga halaman selesai dimuat setelah login
        time.sleep(3)
        return True
    
    except Exception as e:
        log_message("warning", "Tombol 'Masuk' tidak ditemukan! Mencoba refresh halaman...")
        driver.refresh()
        time.sleep(3)
        return False

    

# Fungsi untuk menutup flyer/iklan
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def close_flyer(driver):
    try:
        # Tunggu hingga elemen flyer muncul (jika ada)
        flyer = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "styles_iconClose__ZjGFM"))
        )

        # Jika ditemukan, klik tombol close menggunakan JavaScript
        driver.execute_script("arguments[0].click();", flyer)
        #log_message("info", "Flyer berhasil diklik untuk ditutup.")

        # Tunggu hingga flyer benar-benar hilang dari DOM
        WebDriverWait(driver, 5).until(
            EC.staleness_of(flyer)  # Tunggu elemen hilang dari halaman
        )
        #log_message("info", "Flyer sudah tertutup sepenuhnya.")

    except TimeoutException:
        log_message("info", "Flyer tidak muncul, langsung lanjut ke proses berikutnya.")
    except NoSuchElementException:
        log_message("info", "Flyer tidak ditemukan, lanjutkan proses.")
    except Exception as e:
        log_message("error", f"Error saat mencoba menutup flyer: {e}")

