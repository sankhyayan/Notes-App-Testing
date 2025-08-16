from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import random
import string
import time

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_register_and_login():
    driver = webdriver.Chrome()
    driver.get("https://practice.expandtesting.com/notes/app")

    # Navigate to registration (adjust locator based on page inspection)
    try:
        register_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Create an account"))
        )
        register_link.click()
    except:
        print("Adjust the 'Register' link locator")

    # Fill registration form
    name = "Test User"
    email = f"{generate_random_string()}@example.com"
    password = "password123"
    try:
        driver.find_element(By.ID, "name").send_keys(name)  # Adjust locator
        driver.find_element(By.ID, "email").send_keys(email)  # Adjust locator
        driver.find_element(By.ID, "password").send_keys(password) 
        driver.find_element(By.ID, "confirmPassword").send_keys(password) # Adjust locator
        driver.find_element(By.CSS_SELECTOR, '[data-testid="register-submit"]').click()  # Adjust locator
    except:
        print("Adjust registration form locators")

    # Wait for login page or success
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="login-view"]'))).click()
        print("Navigated to login page")
    except Exception as e:
        print(f"Login page navigation failed: {e}")
        driver.save_screenshot("login_navigation_error.png")

    # Log in
    try:
        driver.find_element(By.ID, "email").send_keys(email)  # Adjust locator
        driver.find_element(By.ID, "password").send_keys(password)  # Adjust locator
        driver.find_element(By.CSS_SELECTOR, '[data-testid="login-submit"]').click()  # Adjust locator
    except:
        print("Adjust login form locators")

    # Wait for notes page
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="add-new-note"]')))

    # Create a note
    try:
        driver.find_element(By.CSS_SELECTOR, '[data-testid="add-new-note"]').click()  # Adjust locator
        driver.find_element(By.ID, "title").send_keys("Test Note")  # Adjust locator
        driver.find_element(By.ID, "description").send_keys("This is a test note")  # Adjust locator
        driver.find_element(By.CSS_SELECTOR, '[data-testid="note-submit"]').click()  # Adjust locator
    except:
        print("Adjust note creation locators")

    driver.implicitly_wait(15)

    # Edit the note
    try:
        note_edit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="note-edit"]')))
        note_edit_button.click()
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "title"))).clear()
        driver.find_element(By.ID, "title").send_keys("Updated Test Note")
        driver.find_element(By.CSS_SELECTOR, '[data-testid="note-submit"]').click()
    except:
        print("Adjust note edit locators")

    driver.implicitly_wait(10)


    # Delete the note
    try:
        xpath = '//button[@data-testid="note-delete" and text()="Delete"]'
        print("Waiting for Delete button to be clickable...")

        try:
            # Wait until the button is clickable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            
            # Retry clicking if stale
            for attempt in range(3):
                try:
                    print(f"Attempt {attempt + 1}: Trying to click Delete button...")
                    driver.find_element(By.XPATH, xpath).click()
                    print("Clicked successfully.")
                    break  # Exit loop if successful
                except StaleElementReferenceException:
                    print("Stale element encountered. Retrying...")
                    time.sleep(1)  # Small delay before retry
            else:
                print("Failed to click Delete button after retries.")

        except TimeoutException:
            print("Delete button not found in time.")
            print("reched here")

        time.sleep(3) 
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="note-delete-confirm"]'))).click()
        time.sleep(10) 
        
    except:
        print("Adjust note delete locator")

    driver.implicitly_wait(10)

    # # Verify deletion
    # notes = driver.find_elements(By.CLASS_NAME, "note")
    # assert not any("Updated Test Note" in note.text for note in notes), "Note deletion failed"

    driver.quit()

if __name__ == "__main__":
    test_register_and_login()
