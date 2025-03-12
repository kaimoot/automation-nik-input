from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import sys
import os
# Add the modules directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .utils import log_message


# Fungsi untuk memilih dan menginisialisasi WebDriver berdasarkan input pengguna
def get_driver(browser_name="chrome", use_headless=False):
    browser_name = browser_name.lower()

    '''
    if use_headless:
        if browser_name == "firefox":
            options.add_argument("--headless")  # Firefox
    else:
        options.add_argument("--headless=new")  # Chrome and Edge
    '''

    if browser_name == "edge":
        log_message("info", "Memulai WebDriver untuk Edge...")
        options = EdgeOptions()
        #options.add_argument("--log-level=3")  # Hanya tampilkan error kritis
        if use_headless:
            options.add_argument("--headless-new")  # Gunakan mode headless jika dipilih
            options.add_argument("--disable-gpu")
            #options.add_argument("--disable-features=ComputePressure")
            #options.add_argument("--disable-software-rasterizer")
            #options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
        # Redirect log Edge WebDriver ke file
        log_path = "webdriver.log"  # Lokasi file log untuk menyimpan output WebDriver
        service = EdgeService(EdgeChromiumDriverManager().install()) #, log_output=open(log_path, "w"))
        return webdriver.Edge(service=service, options=options)

    elif browser_name == "firefox":
        log_message("info", "Memulai WebDriver untuk Firefox...")
        options = FirefoxOptions()
        #options.add_argument("--log-level=3")  # Hanya tampilkan error kritis
        if use_headless:
            options.add_argument("--headless")  # Gunakan mode headless jika dipilih
            options.add_argument("--disable-gpu")
            #options.add_argument("--disable-features=ComputePressure")
            #options.add_argument("--disable-software-rasterizer")
            #options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
        # Redirect log Edge WebDriver ke file
        log_path = "webdriver.log"  # Lokasi file log untuk menyimpan output WebDriver
        service = FirefoxService(GeckoDriverManager().install()) #, log_output=open(log_path, "w"))
        return webdriver.Firefox(service=service, options=options)

    else:  # Default ke Chrome
        log_message("info", "Memulai WebDriver untuk Chrome...")
        options = ChromeOptions()
        #options.add_argument("--log-level=3")  # Hanya tampilkan error kritis
        if use_headless:
            options.add_argument("--headless-new")  # Gunakan mode headless jika dipilih
            options.add_argument("--disable-gpu")
            #options.add_argument("--disable-features=ComputePressure")
            #options.add_argument("--disable-software-rasterizer")
            #options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
        # Redirect log Edge WebDriver ke file
        log_path = "webdriver.log"  # Lokasi file log untuk menyimpan output WebDriver
        service = ChromeService(ChromeDriverManager().install()) #, log_output=open(log_path, "w"))
        return webdriver.Chrome(service=service, options=options)
    

'''
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-3d-apis")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--use-gl=disabled")
options.add_argument("--disable-gpu-driver-bug-workarounds")
options.add_argument("--disable-gpu-process-crash-limit")
options.add_argument("--headless=new")
options.add_argument("--log-level=3")
'''