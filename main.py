from datetime import datetime

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configure Chrome options (optional, customize if needed)
chrome_options = Options()

# Create a new Chrome browser instance
driver = webdriver.Chrome(options=chrome_options)

# Open the Cookie Clicker website
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Wait for the page to load (adjust wait time as needed)
time.sleep(15)  # Adjust this based on your internet speed and page complexity

# Select English language
lang_btn = driver.find_element(By.ID, "langSelect-EN")
lang_btn.click()

time.sleep(3)  # Wait for language change to take effect

# Get references to the cookie element, product container, and product divs
cookie_btn = driver.find_element(By.ID, "bigCookie")
products = driver.find_element(By.ID, "products")
div_elements = products.find_elements(By.CLASS_NAME, "product")

# Track start and end minutes for the 5-minute game duration
start_min = datetime.now().time().minute
end_min = (start_min + 5) % 60  # Calculate end_min efficiently using modulo

def select_cookie_per_second():
    try:
        cookie_score = driver.find_element(By.CSS_SELECTOR, "#cookiesPerSecond").text
        return cookie_score

    except selenium.common.exceptions.StaleElementReferenceException:
        select_cookie_per_second()

is_game_on = True
while is_game_on:
    # Check if current minute matches the end minute (game duration completed)
    if int(datetime.now().time().minute) == end_min:
        # Get current cookies per second
        cookie_per_second = select_cookie_per_second()

        print(f"Cookies {cookie_per_second}")
        is_game_on = False  # Stop the game loop

    # Track start and end seconds for the 5-second product purchase cycle
    start_second = datetime.now().time().second
    end_second = (start_second + 10) % 60  # Efficient end_second calculation

    while is_game_on:
        # Click the cookie to generate cookies
        cookie_btn.click()

        # Check if current second matches the end second (time to purchase product)
        if int(datetime.now().time().second) == end_second:
            # Get a list of currently purchasable product IDs
            enabled_products = [div.get_attribute("id") for div in div_elements if "enabled" in div.get_attribute("class")]

            if len(enabled_products) > 0:
                # Select the most expensive purchasable product
                selected_product = enabled_products[-1]

                # Click the button for the selected product
                product_btn = driver.find_element(By.ID, selected_product)
                product_btn.click()

            # Break out of the inner loop to prevent unnecessary iterations
            break

# Quit the browser after the game is finished
driver.quit()