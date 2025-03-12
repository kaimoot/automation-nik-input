from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Use --headless for older versions
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com")
print(driver.title)
driver.quit()