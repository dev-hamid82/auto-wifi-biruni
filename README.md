# Auto Login Wi-Fi (University of Birjand)

This script automatically logs into the University of Birjand Wi-Fi network using Selenium.

## How to Run

1. **Download the source code**

2. **Install Python dependencies**  
   ```bash
   pip install -r requirements.txt
   apt install python3-selenium

3. **Install WebDriver (GeckoDriver for Firefox)** (
    ```bash
   wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
   tar -xvzf geckodriver-v0.34.0-linux64.tar.gz
   sudo mv geckodriver /usr/local/bin/
   geckodriver --version
 )


4. **edit line 47, 48 for username & password**



5. **Add to startup**

    Move the source to your system's startup folder

    Make sure the script is set as executable

6. **Set delay**

    Configure a 5s delay in startup settings before the script runs




**Notes**

Make sure you have Python 3.x installed.

Your login credentials must be configured correctly in the script.

Tested on Linux.
