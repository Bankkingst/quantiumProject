import os
from webdriver_manager.chrome import ChromeDriverManager

# Download chromedriver and add its directory to PATH so dash_duo can find it
_driver_path = ChromeDriverManager().install()
os.environ["PATH"] = os.path.dirname(_driver_path) + os.pathsep + os.environ["PATH"]
