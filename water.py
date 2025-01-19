import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import re
import concurrent.futures
from tqdm import tqdm
import tkinter as tk
from tkinter import ttk,messagebox
import threading
import queue

# Sample form_data (this should be replaced with actual form data as required)



def create_driver():
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")  # Use the latest headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size to avoid detection issues
    
    # Optimize performance
    chrome_options.add_argument("--disable-extensions")  # Disable extensions to speed up
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    chrome_options.add_argument("--disable-software-rasterizer")  # Avoid software rendering
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable loading images
    chrome_options.add_argument("--enable-automation")  # Indicate automation use
    chrome_options.add_argument("--disable-infobars")  # Disable 'Chrome is being controlled' message
    
    # Additional security & detection prevention
    chrome_options.add_argument("--disable-popup-blocking")  # Prevent blocking popups
    chrome_options.add_argument("--incognito")  # Run in incognito mode for cleaner sessions
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36")  # Set user agent to reduce detection

    # Enable logging for debugging purposes (optional)
    chrome_options.add_argument("--log-level=3")  # Minimize logging output (DEBUG=0, INFO=1, WARNING=2, ERROR=3)
    
    # Return the initialized driver
    return webdriver.Chrome(options=chrome_options)

def fill_field(driver, wait, xpath, value):
    try:
        field = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        field.clear()
        field.send_keys(value)
        print(f"Filled field at {xpath} with value: {value}")
    except Exception as e:
        print(f"Error filling field at {xpath}: {str(e)}")


def handle_cherokeecountyga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
        
            
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[1]/div/input": form_data["email"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[2]/div/input": form_data["name"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[3]/div/input": form_data["phone"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[4]/div/textarea": form_data["address"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[1]/div/div/input": form_data["city"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[3]/div/div/input": form_data["zip"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[6]/div/input": form_data["company"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[1]/div[2]/div[1]/div[2]/div/div[1]"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[2]/div/div/div/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Alabama")  # Adjust text as per available options
        print("Selected dropdown option")

                    # Handle dropdown selection (corrected)
        dropdown2_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[1]/div[4]/div/div/div/div/div[1]/input"
        dropdown2 = wait.until(EC.presence_of_element_located((By.XPATH, dropdown2_xpath)))



   # Clear the dropdown input field
        dropdown2.clear()

# Enter the desired option into the input field
        dropdown2.send_keys("County Marshal")
        print("Typed 'Library' into the dropdown")

# Press Enter to confirm the selection
        dropdown2.send_keys(Keys.ENTER)
        print("Pressed Enter to select 'County Marshal'")
        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[3]/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_albanyga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[16]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Handle checkboxes
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[18]/div/div[1]/div/div/div/div/div/div/div"
        checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox1_xpath)))
        driver.execute_script("arguments[0].click();", checkbox)
        print(f"Checked {checkbox1_xpath}")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")

        # Delay of 15 seconds after form submission
        time.sleep(60)

        # Extract confirmation message
        try:
            confirmation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Your security key is')]").text
            security_key = re.search(r"Your security key is (\S+)", confirmation_message).group(1)
            reference_number = re.search(r"Your request reference number is (\S+)", confirmation_message).group(1)
            return {"status": "Success", "confirmation": "Form submitted", "reference_number": reference_number, "security_key": security_key}
        except NoSuchElementException:
            print("Confirmation message not found")
            return {"status": "Success", "confirmation": "Form submitted", "reference_number": "", "security_key": ""}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}
    

def handle_collegeparkga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[3]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_cityofaugustaga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
        
            
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[1]/div/input": form_data["email"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[2]/div/input": form_data["name"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[3]/div/input": form_data["phone"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[4]/div/textarea": form_data["address"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[1]/div/div/input": form_data["city"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[3]/div/div/input": form_data["zip"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[6]/div/input": form_data["company"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[1]/div[2]/div[1]/div[2]/div/div[1]"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[2]/div/div/div/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Alabama")  # Adjust text as per available options
        print("Selected dropdown option")
#checkbox
        checkbox1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[3]/div[2]/div/div/input"
        for checkbox_xpath in [checkbox1_xpath]:
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"Checked {checkbox_xpath}")
        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")
        # Submit form
        submit_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[4]/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}

def handle_cityoffayettevillega_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[1]/div/input": form_data["email"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[2]/div/input": form_data["name"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[3]/div/input": form_data["phone"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[4]/div/textarea": form_data["address"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[1]/div/div/input": form_data["city"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[3]/div/div/input": form_data["zip"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[6]/div/input": form_data["company"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[1]/div[2]/div[1]/div[2]/div/div[1]"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle department dropdown/autocomplete
        dropdown1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[1]/div[4]/div/div/div/div/div[1]/input"
        dropdown1 = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
        
        # Clear existing value
        dropdown1.clear()
        
        # Click to focus
        dropdown1.click()
        time.sleep(1)
        
        # Type value
        dropdown1.send_keys("City Hall")
        time.sleep(1)
        
        # Press down arrow and enter to select from autocomplete
        actions = ActionChains(driver)
        actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
        time.sleep(1)
        print("Entered 'City Hall' in department field")

        # Handle state dropdown
        dropdown2_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[2]/div/div/div/select"
        dropdown2 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown2_xpath))))
        dropdown2.select_by_visible_text("Alabama")
        print("Selected state dropdown option")

        # Handle checkbox
        checkbox1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[3]/div[2]/div/div/input"
        checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox1_xpath)))
        driver.execute_script("arguments[0].click();", checkbox)
        print("Checked agreement checkbox")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[4]/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_peachtreecitygapolice_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
        
            
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[1]/div/input": form_data["email"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[2]/div/input": form_data["name"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[3]/div/input": form_data["phone"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[4]/div/textarea": form_data["address"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[1]/div/div/input": form_data["city"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[3]/div/div/input": form_data["zip"],
            "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[6]/div/input": form_data["company"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[1]/div[2]/div[1]/div[2]/div/div[1]"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[2]/div/div/div/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Alabama")  # Adjust text as per available options
        print("Selected dropdown option")

                    # Handle dropdown selection (corrected)
        dropdown2_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[1]/div[4]/div/div/div/div/div[1]/input"
        dropdown2 = wait.until(EC.presence_of_element_located((By.XPATH, dropdown2_xpath)))



   # Clear the dropdown input field
        dropdown2.clear()

# Enter the desired option into the input field
        dropdown2.send_keys("Library")
        print("Typed 'Library' into the dropdown")

# Press Enter to confirm the selection
        dropdown2.send_keys(Keys.ENTER)
        print("Pressed Enter to select 'Library'")
        # check
        checkbox1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[3]/div[2]/div/div/input"
        for checkbox_xpath in [checkbox1_xpath]:
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"Checked {checkbox_xpath}")
        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[4]/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}



def handle_unioncityga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[3]/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")
        
        #checkbox
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div[1]/div/div/div/div/div/div/div"
        for checkbox_xpath in [checkbox1_xpath]:
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"Checked {checkbox_xpath}")
      

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button/div"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_maconbibbcountyga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["name"],       
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/input": form_data["zip"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["phone"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[14]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "//html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[15]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button/div"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")

        # Delay of 15 seconds after form submission
        time.sleep(60)

        # Extract confirmation message
        # Extract confirmation message
        try:
            confirmation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Your security key is')]").text
            security_key = re.search(r"Your security key is (\S+)", confirmation_message).group(1)
            reference_number = re.search(r"Your request reference number is (\S+)", confirmation_message).group(1)
            return {"status": "Success", "confirmation": "Form submitted", "reference_number": reference_number, "security_key": security_key}
        except NoSuchElementException:
            print("Confirmation message not found")
            return {"status": "Success", "confirmation": "Form submitted", "reference_number": "", "security_key": ""}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_cantonga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[1]/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[2]/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[3]/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button/div"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")

        # Delay of 15 seconds after form submission
        time.sleep(60)

        # Extract confirmation message
        # Extract confirmation message
        try:
            confirmation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Your security key is')]").text
            security_key = re.search(r"Your security key is (\S+)", confirmation_message).group(1)
            reference_number = re.search(r"Your request reference number is (\S+)", confirmation_message).group(1)
            return {"status": "Success", "confirmation": "Form submitted", "reference_number": reference_number, "security_key": security_key}
        except NoSuchElementException:
            print("Confirmation message not found")
            return {"status": "Success", "confirmation": "Form submitted", "reference_number": "", "security_key": ""}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}
    
def handle_hapevillega_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[1]/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[3]/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[2]/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")
        
        #checkbox
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div[1]/div/div/div/div/div/div/div"
        for checkbox_xpath in [checkbox1_xpath]:
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"Checked {checkbox_xpath}")
      

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button/div"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}
    
def handle_fairburnga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        #checkbox
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/div/div/div/div/div/div/div"
        for checkbox_xpath in [checkbox1_xpath]:
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"Checked {checkbox_xpath}")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_eastpointga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[15]/div/div[1]/div/div/div/div/div/div/div"
        for checkbox_xpath in [checkbox1_xpath]:
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"Checked {checkbox_xpath}")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")

        # Delay of 15 seconds after form submission
        time.sleep(60)

        # Extract confirmation message
        confirmation_message = driver.find_element(By.XPATH, "//*[contains(text(), 'Your request reference number')]").text
        reference_number = re.search(r"Your request reference number is (\S+)", confirmation_message).group(1)
        security_key = re.search(r"Your security key is (\S+)", confirmation_message).group(1)

        return {"status": "Success", "confirmation": "Form submitted", "reference_number": reference_number, "security_key": security_key}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}

    

def handle_woodstockga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[1]/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[3]/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[2]/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("View Only")  # Adjust text as per available options
        print("Selected dropdown option")
      

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button/div"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}



def handle_spaldingcountyga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}

def handle_riverdalega_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[1]/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[2]/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[3]/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_acworthga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[1]/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[2]/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[3]/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_austellga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}



def handle_forestparkga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_roswellga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")
        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button/div"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}
    

def handle_conyersga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        #checkbox
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div[1]/div/div/div/div/div/div/div"
        for checkbox_xpath in [checkbox1_xpath]:
            checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
            driver.execute_script("arguments[0].click();", checkbox)
            print(f"Checked {checkbox_xpath}")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[4]/div/button"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}



def handle_cityofgriffin_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[1]/vi-form-field-edit/vi-field-fullname-edit/div/span[1]/input": form_data["first name"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[1]/vi-form-field-edit/vi-field-fullname-edit/div/span[2]/input": form_data["last name"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[4]/vi-form-field-edit/vi-field-email-edit/div/input": form_data["email"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[3]/vi-form-field-edit/vi-field-phone-edit/div/span/input": form_data["phone"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/div[2]/ol/li[2]/input": form_data["email"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[2]/vi-form-field-edit/vi-field-fulladdress-edit/div/span[1]/input": form_data["address"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[2]/vi-form-field-edit/vi-field-fulladdress-edit/div/span[2]/input": form_data["unit number"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[2]/vi-form-field-edit/vi-field-fulladdress-edit/div/span[3]/span[1]/input": form_data["city"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[2]/vi-form-field-edit/vi-field-fulladdress-edit/div/span[3]/span[2]/input": form_data["state"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[2]/vi-form-field-edit/vi-field-fulladdress-edit/div/span[4]/input": form_data["zip"],
            "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[2]/vi-form-field-edit/vi-field-fulladdress-edit/div/span[5]/input": form_data["country"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[5]/vi-form-field-edit/vi-field-paragraphtext-edit/div/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/div/form-builder-submit-pagination/div/div[6]/vi-form-field-edit/vi-field-singledropdown-edit/div/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Yes")  # Adjust text as per available options
        print("Selected dropdown option")
      

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div[2]/div/div[2]/div[3]/div[2]/section/div/form/div/form-builder-submit-actions/div/a[2]"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}



def handle_henrycounty_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[3]/div/div/div[2]/div/input": form_data["first name"],
            "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[4]/div/div/div[2]/div/input": form_data["last name"],
            "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[6]/div/div/div[2]/div/input": form_data["email"],
            "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[11]/div/div/div[2]/div/input": form_data["phone"],
            "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[7]/div/div/div[2]/div/input": form_data["address"],
            "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[8]/div/div/div[2]/div/input": form_data["city"],
            "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[9]/div/div/div[2]/div/input": form_data["state"],
            "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[10]/div/div/div[2]/div/input": form_data["zip"],
          
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[3]/div/div/div/div[13]/div/div/div[2]/textarea[1]"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")

        # Submit form
        submit_xpath = "/html/body/div/ob-bottom-navigation/div/div[1]/section/div/div/form/div/div[4]/button[2]/span/span"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def handle_formsite_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/form/div[2]/div[6]/input": form_data["date"],
            "/html/body/form/div[2]/div[9]/input": form_data["name"],
            "/html/body/form/div[2]/div[22]/input": form_data["phone"],
            "/html/body/form/div[2]/div[21]/input": form_data["email"],
            "/html/body/form/div[2]/div[14]/input": form_data["address"],
            "//html/body/form/div[2]/div[17]/input": form_data["city"],
            "/html/body/form/div[2]/div[19]/input": form_data["zip"],
            "/html/body/form/div[2]/div[30]/input": form_data["date"],
            "/html/body/form/div[2]/div[40]/input": form_data["address"],
            "/html/body/form/div[2]/div[42]/input": form_data["city"],
            "/html/body/form/div[2]/div[44]/input": form_data["zip"],
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/form/div[2]/div[26]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle first dropdown
        try:
            dropdown0_xpath = "/html/body/form/div[2]/div[24]/select"
            dropdown0 = wait.until(EC.presence_of_element_located((By.XPATH, dropdown0_xpath)))
            select0 = Select(dropdown0)
            
            # Wait for options to load
            time.sleep(2)
            
            # Get available options
            options = [o for o in select0.options if o.text.strip()]
            if options:
                select0.select_by_visible_text(options[-1].text)  # Select last non-empty option
                print(f"Selected {options[-1].text} from first dropdown")
            else:
                print("No valid options found in first dropdown")
                
        except Exception as e:
            print(f"Error handling first dropdown: {str(e)}")
            driver.save_screenshot("dropdown0_error.png")

        # Handle state dropdowns
        for dropdown_xpath in ["/html/body/form/div[2]/div[18]/select", 
                             "/html/body/form/div[2]/div[43]/select"]:
            try:
                dropdown = wait.until(EC.presence_of_element_located((By.XPATH, dropdown_xpath)))
                select = Select(dropdown)
                
                # Wait for options to load
                time.sleep(2)
                
                # Try multiple selection methods
                try:
                    select.select_by_visible_text("Alabama")
                except:
                    try:
                        select.select_by_value("AL")
                    except:
                        try:
                            # Get all non-empty options
                            options = [o for o in select.options if o.text.strip()]
                            if options:
                                select.select_by_visible_text(options[1].text)  # Select first non-empty option
                            else:
                                print(f"No valid options found in dropdown {dropdown_xpath}")
                        except:
                            print(f"Could not select state in dropdown {dropdown_xpath}")
                            
                print(f"Handled state selection for {dropdown_xpath}")
                
            except Exception as e:
                print(f"Error handling state dropdown {dropdown_xpath}: {str(e)}")
                driver.save_screenshot(f"dropdown_error_{dropdown_xpath.replace('/', '_')}.png")

        # Handle checkboxes
        checkbox_xpaths = [
            "/html/body/form/div[2]/div[7]/table/tbody/tr[2]/td/label",
            "/html/body/form/div[2]/div[31]/table/tbody/tr[1]/td/label",
            "/html/body/form/div[2]/div[33]/table/tbody/tr[1]/td/label",
            "/html/body/form/div[2]/div[35]/table/tbody/tr[1]/td/label"
        ]
        
        for checkbox_xpath in checkbox_xpaths:
            try:
                checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, checkbox_xpath)))
                driver.execute_script("arguments[0].click();", checkbox)
                print(f"Checked {checkbox_xpath}")
                time.sleep(1)  # Add small delay between checkbox clicks
            except Exception as e:
                print(f"Error checking checkbox {checkbox_xpath}: {str(e)}")
                driver.save_screenshot(f"checkbox_error_{checkbox_xpath.replace('/', '_')}.png")

        # Take screenshot before submission
        driver.save_screenshot("before_submit.png")
        
        # Submit form
        submit_xpath = "/html/body/form/div[3]/div/input"
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, submit_xpath)))
        driver.execute_script("arguments[0].click();", submit_button)
        print("Clicked submit button")
        
        # Wait for submission to complete
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


def save_results(results, filename="submission3_results.csv"):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'status', 'confirmation', 'error'])
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")



def process_form(url,retries=3):
    for attempt in range(retries):
        driver = create_driver()
        wait = WebDriverWait(driver, 20)
        driver.get(url)
        
    try:
        if url == "https://cherokeecountyga.nextrequest.com/requests/new":
            result = handle_cherokeecountyga_form(driver, url)
        elif url == "https://albanyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_albanyga_form(driver, url)
        elif url == "https://collegeparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_collegeparkga_form(driver, url)
        elif url == "https://cityofaugustaga.nextrequest.com/requests/new":
            result = handle_cityofaugustaga_form(driver, url)
        elif url == "https://cityoffayettevillega.nextrequest.com/requests/new":
            result = handle_cityoffayettevillega_form(driver, url)
        elif url == "https://peachtreecitygapolice.nextrequest.com/requests/new":
            result = handle_peachtreecitygapolice_form(driver, url)
        elif url == "https://unioncityga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_unioncityga_form(driver, url)
        elif url == "https://maconbibbcountyga.justfoia.com/Forms/Launch/a709d888-de2f-4857-9c82-b12b2645a87c":
            result = handle_maconbibbcountyga_form(driver, url)
        elif url == "https://cantonga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_cantonga_form(driver, url)
        elif url == "https://hapevillega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_hapevillega_form(driver, url)
        elif url == "https://fairburnga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_fairburnga_form(driver, url)
        elif url == "https://eastpointga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_eastpointga_form(driver, url)
        elif url == "https://woodstockga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_woodstockga_form(driver, url)
        elif url == "https://spaldingcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_spaldingcountyga_form(driver, url)
        elif url == "https://riverdalega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_riverdalega_form(driver, url)
        elif url == "https://acworthga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_acworthga_form(driver, url)
        elif url == "https://austellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_austellga_form(driver, url)
        elif url == "https://forestparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_forestparkga_form(driver, url)
        elif url == "https://roswellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_roswellga_form(driver, url)
        elif url == "https://conyersga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_conyersga_form(driver, url)
        elif url == "https://www.cityofgriffin.com/services/open-records":
            result = handle_cityofgriffin_form(driver, url)
        elif url == "https://henrycounty-services.app.transform.civicplus.com/forms/34175":
            result = handle_henrycounty_form(driver, url)
        elif url == "https://fs6.formsite.com/mAFRD/jiupubq3at/index.html":
            result = handle_formsite_form(driver, url)
        else:
            result = {"status": "unknown", "confirmation": "", "error": "Unknown URL"}
    except Exception as e:
        print(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
        result = {"status": "failed", "confirmation": "", "error": str(e)}
        time.sleep(5) 
    finally:
        driver.quit()
    
    return result

def save_results(results, filename="submission3_results.csv"):
    import csv
    keys = results[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)



def update_progress_bar(progress_bar, progress_var, value):
    progress_var.set(value)
    progress_bar.update_idletasks()

def run_processing(urls, results, progress_queue):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(process_form, url): url for url in urls}
        for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append({"url": url, "status": result["status"], "confirmation": result.get("confirmation", ""), "error": result.get("error", "")})
            except Exception as e:
                results.append({"url": url, "status": "failed", "confirmation": "", "error": str(e)})
            progress_queue.put(i + 1)

    # Save results
    save_results(results)

    # Signal that processing is complete
    progress_queue.put(None)

def create_gradient(canvas, width, height):
    for i in range(height):
        grey_value = int(200 - (i * 100 / height))
        color = f'#{grey_value:02x}{grey_value:02x}{grey_value:02x}'
        canvas.create_line(0, i, width, i, fill=color)

def resize_canvas(event):
    create_gradient(event.widget, event.width, event.height)

def submit_form():
    global form_data
    form_data = {
        "date": date_entry.get(),
        "name": name_entry.get(),
        "first name": first_name_entry.get(),
        "last name": last_name_entry.get(),
        "phone": phone_entry.get(),
        "email": email_entry.get(),
        "address": address_entry.get(),
        "city": city_entry.get(),
        "state": state_entry.get(),
        "zip": zip_entry.get(),
        "company": company_entry.get(),
        "case": case_entry.get(),
        "time": time_entry.get(),
        "person represented": person_represented_entry.get(),
        "case number": case_number_entry.get(),
        "unit number": unit_number_entry.get(),
        "country": country_entry.get(),
        "message": message_entry.get("1.0", tk.END)
    }
    
    # Check if all fields are filled
    for key, value in form_data.items():
        if not value.strip():
            messagebox.showerror("Error", f"Please fill in the {key} field.")
            return
    
    selected_counties = [county for county, var in county_vars.items() if var.get()]
    if not selected_counties:
        messagebox.showerror("Error", "Please select at least one county.")
        return
    
    # Create a new window for the progress bar
    global progress_window, progress_var, progress_bar, progress_queue
    progress_window = tk.Toplevel(root)
    progress_window.title("Processing Progress")
    
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_window, variable=progress_var, maximum=len(selected_counties))
    progress_bar.pack(pady=20, padx=20)
    
    progress_queue = queue.Queue()
    
    def process_queue():
        try:
            value = progress_queue.get_nowait()
            if value is None:
                progress_window.quit()
            else:
                update_progress_bar(progress_bar, progress_var, value)
            progress_window.after(100, process_queue)
        except queue.Empty:
            progress_window.after(100, process_queue)
    
    process_queue()
    
    for county in selected_counties:
        if county in urls:
            threading.Thread(target=run_processing, args=(urls[county], results, progress_queue)).start()

def draw_form_fields():
    global entries
    entries = {}
    x_position = 50
    y_position = 50
    for i, (field, var_name) in enumerate([
        ("Date", "date_entry"),
        ("Name", "name_entry"),
        ("First Name", "first_name_entry"),
        ("Last Name", "last_name_entry"),
        ("Phone", "phone_entry"),
        ("Email", "email_entry"),
        ("Address", "address_entry"),
        ("City", "city_entry"),
        ("State", "state_entry"),
        ("Zip", "zip_entry"),
        ("Company", "company_entry"),
        ("Case", "case_entry"),
        ("Time", "time_entry"),
        ("Person Represented", "person_represented_entry"),
        ("Case Number", "case_number_entry"),
        ("Unit Number", "unit_number_entry"),
        ("Country", "country_entry"),
        ("Message", "message_entry")
    ]):
        label = ttk.Label(root, text=field)
        canvas.create_window(x_position, y_position, window=label, anchor="w")
        if field == "Message":
            entry = tk.Text(root, height=5, width=50)
        else:
            entry = ttk.Entry(root)
        canvas.create_window(x_position + 200, y_position, window=entry, anchor="w")
        entries[var_name] = entry

        if (i + 1) % 3 == 0:
            x_position = 50
            y_position += 70 if field != "Message" else 100
        else:
            x_position += 400

    global date_entry, name_entry, first_name_entry, last_name_entry, phone_entry, email_entry, address_entry, city_entry, state_entry, zip_entry, company_entry, case_entry, time_entry, person_represented_entry, case_number_entry, unit_number_entry, country_entry, message_entry
    date_entry = entries["date_entry"]
    name_entry = entries["name_entry"]
    first_name_entry = entries["first_name_entry"]
    last_name_entry = entries["last_name_entry"]
    phone_entry = entries["phone_entry"]
    email_entry = entries["email_entry"]
    address_entry = entries["address_entry"]
    city_entry = entries["city_entry"]
    state_entry = entries["state_entry"]
    zip_entry = entries["zip_entry"]
    company_entry = entries["company_entry"]
    case_entry = entries["case_entry"]
    time_entry = entries["time_entry"]
    person_represented_entry = entries["person_represented_entry"]
    case_number_entry = entries["case_number_entry"]
    unit_number_entry = entries["unit_number_entry"]
    country_entry = entries["country_entry"]
    message_entry = entries["message_entry"]

    # Create checkboxes for selecting counties at the bottom in horizontal form
    global county_vars
    county_vars = {}
    x_position = 50
    y_position += -10  # Adjusted y_position to avoid collision with other fields
    for county in urls.keys():
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(root, text=county, variable=var)
        canvas.create_window(x_position, y_position, window=checkbox, anchor="w")
        county_vars[county] = var
        x_position += 200
        if x_position > 800:
            x_position = 50
            y_position += 30

    submit_button = ttk.Button(root, text="Submit", command=submit_form)
    canvas.create_window(300, y_position + 50, window=submit_button, anchor="w")

if __name__ == "__main__":
    results = []

    # Dictionary of URLs classified by county
    urls = {
    "Bibb County": [
        "https://maconbibbcountyga.justfoia.com/Forms/Launch/a709d888-de2f-4857-9c82-b12b2645a87c"
    ],
    "Cherokee County": [
        "https://cherokeecountyga.nextrequest.com/requests/new",
        "https://cantonga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://woodstockga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb"
    ],
    "Clayton County": [
        "https://claytoncountywaterauthority.wufoo.com/forms/z1e6l46517vub7j/"
    ],
    "Cobb County": [
        "https://austellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://smyrnaga.justfoia.com/Forms/Launch/fd208f47-7557-4edf-9478-723c87ba6b30"
    ],
    "Dougherty County": [
        "https://albanyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb"
    ],
    "Fayette County": [
        "https://cityoffayettevillega.nextrequest.com/requests/new"
    ],
    "Forsyth County": [
        "https://forsythcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb"
    ],
    "Fulton County": [
        "https://roswellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://fairburnga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://collegeparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb"
    ],
    "Henry County": [
        "https://henrycounty-services.app.transform.civicplus.com/forms/34175"
    ],
    "Richmond County": [
        "https://cityofaugustaga.nextrequest.com/requests/new"
    ],
    "Rockdale County": [
        "https://conyersga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb"
    ],
    "Spalding County": [
        "https://spaldingcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://www.cityofgriffin.com/services/open-records"
    ]
}

    # Create the main window
    root = tk.Tk()
    root.title("Form Submission Progress")

    # Create a canvas
    canvas = tk.Canvas(root, width=1000, height=1000)
    canvas.pack(fill="both", expand=True)

    # Create the gradient background
    create_gradient(canvas, 1000, 1000)
    canvas.bind("<Configure>", resize_canvas)

    draw_form_fields()

    root.mainloop()