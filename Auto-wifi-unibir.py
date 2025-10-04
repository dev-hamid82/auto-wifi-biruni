#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess, time, re, os

# Send Notification ------------------------------------
def notify(title, message):
    env = os.environ.copy()
    if "DBUS_SESSION_BUS_ADDRESS" not in env:

        try:
            user = os.environ.get("USER")
            pid = subprocess.check_output(
                ["pgrep", "-u", user, "gnome-session"], text=True
            ).splitlines()[0]
            environ = subprocess.check_output(
                ["tr", "\0", "\n"], input=open(f"/proc/{pid}/environ", "rb").read()
            ).decode()
            for line in environ.splitlines():
                if line.startswith("DBUS_SESSION_BUS_ADDRESS="):
                    env["DBUS_SESSION_BUS_ADDRESS"] = line.split("=",1)[1]
                    break
        except:
            pass
    subprocess.run(["notify-send", title, message], env=env)
    time.sleep(0.5)

# Turn On WIFI ------------------------------------
wifi_status = subprocess.run(["nmcli", "radio", "wifi"], capture_output=True, text=True).stdout.strip()
if wifi_status.lower() == "disabled":
    # print("[*] Wi-Fi is off, turning it on...")
    subprocess.run(["nmcli", "radio", "wifi", "on"])
    time.sleep(2)
else:
    pass

# SSIDs ------------------------------------
WIFI_SSIDS = ["SARV I", "SARV II", "SARV III", "SARV IV", "Network", "Amir", "Sadaf I", "Sadaf II", "Sadaf III", "Sadaf IV", "Sardar", "Abouzar", "Tohid"]
WIFI_PASSWORD = ""

# Captive Portal ------------------------------------
USERNAME = "student-number"
PASSWORD = "password"
LOGIN_URL = "http://neverssl.com"

# Find SSID ------------------------------------
# print("[*] Scanning for available Wi-Fi networks...")
time.sleep(3)
available_ssids = subprocess.run(["nmcli", "-t", "-f", "SSID", "device", "wifi", "list"],
                                 capture_output=True, text=True).stdout.splitlines()
available_ssids = [s.strip() for s in available_ssids if s.strip()]

ssid_to_connect = None
for ssid in WIFI_SSIDS:
    if ssid in available_ssids:
        ssid_to_connect = ssid
        break

if ssid_to_connect is None:
    # print("[-] No known SSID available. Exiting.")
    exit(1)

# print(f"[*] Connecting to Wi-Fi: {ssid_to_connect}")
subprocess.run(["nmcli", "device", "wifi", "connect", ssid_to_connect, "password", WIFI_PASSWORD])
time.sleep(3)
# print(f"[+] Connected to {ssid_to_connect}")
notify("🛜 Wi-Fi Status", f"✅ Connecting : {ssid_to_connect} ...")

# Open FireFox ------------------------------------
firefox_options = Options()
firefox_options.add_argument("--headless")  # in background
service = Service("/usr/local/bin/geckodriver")
driver = webdriver.Firefox(service=service, options=firefox_options)
wait = WebDriverWait(driver, 25)

# Captive Portal Login ------------------------------------
driver.get(LOGIN_URL)
username_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
password_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "loginButton")))

# print("[*] Filling login form...")
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
login_button.click()
time.sleep(2)
# notify("🛜 Wi-Fi Status", "✅ Captive Portal logged in")

ping_success = False
for i in range(3):
    ret = subprocess.run(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.DEVNULL)
    if ret.returncode == 0:
        ping_success = True
        break
    time.sleep(1)

if ping_success:
    # print("[+] Internet connected successfully!")
    notify("🛜 Wi-Fi Status", "✅ WiFi connected successfully")
else:
    # print("[-] Internet connection failed.")
    notify("🛜 Wi-Fi Status", "❌ WiFi connection failed")


# Remaining Internet ------------------------------------
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[-1])
driver.get("https://sib.birjand.ac.ir/users/")
time.sleep(6)


wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "MainBox")))
time.sleep(5)


try:
    ul_elements = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.ChartLegend"))
    )
except:
    
    notify("🛜 Wi-Fi Status", "❌ WiFi connection failed")
    driver.quit()
    exit()


last_ul = ul_elements[-1]


li_elements = last_ul.find_elements(By.CSS_SELECTOR, "li.dLi")
if len(li_elements) < 3:

    driver.quit()
    exit()


third_li_text = li_elements[2].text


match = re.search(r"(\d+)\s*گیگ", third_li_text)
if match:
    remaining_gb = match.group(1)
    remaining_text = f"{remaining_gb} GB 〽️"
    # print("[+] Remaining:", remaining_text)
    notify("🛜 Remaining Internet", remaining_text)
else:
    notify("🛜 Wi-Fi Status", "❌ WiFi connection failed")
    # print("[-] Not Found")


# Close FireFox ------------------------------------
driver.quit()
# print("[*] Done!")


# coded by hamid :)
