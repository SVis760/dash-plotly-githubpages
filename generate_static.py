import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from app import app  # Import your Dash app

def save_static_html():
    """Launch Dash app, visit it with Selenium, and save the page as HTML."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Automatically install Chrome and ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Start the Dash app in a background thread
        from threading import Thread
        server_thread = Thread(target=lambda: app.run_server(debug=False, port=8050, use_reloader=False))
        server_thread.start()
        
        # Wait for the app to start
        time.sleep(5)

        # Visit the page and ensure the static folder exists
        driver.get("http://127.0.0.1:8050")

        # Ensure 'static' directory exists
        os.makedirs("static", exist_ok=True)

        # Save the page source
        with open("static/index.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    finally:
        driver.quit()

if __name__ == "__main__":
    save_static_html()
