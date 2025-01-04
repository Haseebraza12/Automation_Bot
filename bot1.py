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

# Sample form_data (this should be replaced with actual form data as required)
form_data = {
    "date":"13/12/2024",
  "name": "John Doe",
  "first name": "Joe",
    "last name":"Doe",
    "phone": "123-456-7890",
    "p1": "123",
    "p2":"456",
    "p3":"7890",
    "email": "dummyemail@example.com",
    "address": "123 Main Street, Suite 100",
    "city": "SampleCity",
    "state": "SampleState",
    "zip": "12345",
    "company":"no",
     "time":"7:25 pm",
     "case":"no",
     "person represented":"no",
     "case number":"12",
     "unit number": "12",
    "country": "USA",
    "message": """My name is John Doe, and I am requesting records from the Code Enforcement Office.

In accordance with the [Insert Local Open Records Act], I am requesting a list of all open code violations for residential properties over the past 30 days. Specifically, I am interested in violations related to damaged or decayed roofs, mold, broken windows, boarded-up windows and doors, overgrown weeds and grass, trash and debris, rodent infestations or unsanitary conditions, flaking or peeling paint, vacant and unsecured structures, and any buildings deemed dangerous, uninhabitable, or unfit for occupancy.

Please provide the details of these violations, including the nature of the violation, the address of the property, and the date of the violation. If possible, I would appreciate receiving the information in a digital format, such as a .csv file or a searchable PDF. However, I am happy to accept the information in any format that is convenient for your office.

Thank you for your assistance in this matter.

Sincerely,
John Doe"""
}
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
def handle_tucker_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

          # Handle dropdown selection
        dropdown0_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/select"
        dropdown0 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown0_xpath))))
        available_options = [o.text for o in dropdown0.options]
        print("Available options in dropdown:", available_options)
        dropdown0.select_by_visible_text("Phone")  # Adjust text if necessary
        print("Selected 'Other inquiries' from dropdown")

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)
        
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Other inquiries")  # Adjust text if necessary
        print("Selected 'Other inquiries' from dropdown")

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle checkboxes
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[15]/div/div[1]/div/div/div/div/div/div/div"
        checkbox2_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[16]/div/div[1]/div/div/div/div/div/div/div"
        for checkbox_xpath in [checkbox1_xpath, checkbox2_xpath]:
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

def handle_doravillega_form(driver, url):
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

        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[18]/div/div[1]/div/div/div/div/div/div/div"
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


def handle_cityofmorrowga_form(driver, url):
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

def handle_kennesawga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/input": form_data["date"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[14]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[16]/div/div[1]/div/div/div/div/div/div/div"
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

def handle_smyrnaga_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["first name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["last name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[16]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[15]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review/inspect")  # Adjust text as per available options
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

def handle_tyronega_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 30)

        # Wait for page to load completely
        time.sleep(7)
        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Library")  # Adjust text as per available options
        print("Selected dropdown option")

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[14]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[15]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[17]/div/div[1]/div/div/div/div/div/div/div"
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
   

def handle_forsythcountyga_form(driver, url):
 
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["email"],
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
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[14]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")

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
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

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

def handle_powderspringsga_form(driver, url):
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
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")
        #checkbox
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/div/div/div/div/div/div/div"
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

def handle_stockbridgega_form(driver, url):
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["phone"],
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
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/div/div/div/div/div/div/div"
        checkbox2_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/div/div/div/div/div/div/div"
        checkbox3_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[14]/div/div[1]/div/div/div/div/div/div/div"
        checkbox4_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[15]/div/div[1]/div/div/div/div/div/div/div"
        for checkbox_xpath in [checkbox1_xpath, checkbox2_xpath,checkbox3_xpath,checkbox4_xpath]:
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

def handle_cityofstonecrestga_form(driver, url):
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
        try:
            dropdown1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[2]/div/div/div/select"
            dropdown1 = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
            
            # Click to open dropdown
            dropdown1.click()
            time.sleep(1)
            
            # Create Select object
            select = Select(dropdown1)
            
            # Print available options for debugging
            available_options = [o.text.strip() for o in select.options]
            print("Available options in dropdown:", available_options)
            
            # Select Alabama using multiple methods
            try:
                select.select_by_visible_text("Alabama")
            except:
                try:
                    select.select_by_value("AL")
                except:
                    try:
                        select.select_by_index(1)
                    except:
                        driver.execute_script("arguments[0].value = 'Alabama';", dropdown1)
            
            # Force change event and ensure selection
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", dropdown1)
            time.sleep(1)
            
            # Additional fallback using ActionChains
            if select.first_selected_option.text != "Alabama":
                actions = ActionChains(driver)
                actions.move_to_element(dropdown1).click().send_keys("Alabama").send_keys(Keys.ENTER).perform()
                time.sleep(1)
            
            print("Selected Alabama from dropdown")
            print(f"Currently selected option: {select.first_selected_option.text}")
            
        except Exception as e:
            print(f"Error handling dropdown: {str(e)}")
            driver.save_screenshot("dropdown_error.png")
       
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

def handle_cityofclarkstonga_form(driver, url):
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
        try:
            dropdown1_xpath = "/html/body/main/div/main/section/div/div[1]/form/div[2]/div[5]/div[2]/div/div/div/select"
            dropdown1 = wait.until(EC.element_to_be_clickable((By.XPATH, dropdown1_xpath)))
            
            # Click to open dropdown
            dropdown1.click()
            time.sleep(1)
            
            # Create Select object
            select = Select(dropdown1)
            
            # Print available options for debugging
            available_options = [o.text.strip() for o in select.options]
            print("Available options in dropdown:", available_options)
            
            # Select Alabama using multiple methods
            try:
                select.select_by_visible_text("Alabama")
            except:
                try:
                    select.select_by_value("AL")
                except:
                    try:
                        select.select_by_index(1)
                    except:
                        driver.execute_script("arguments[0].value = 'Alabama';", dropdown1)
            
            # Force change event and ensure selection
            driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", dropdown1)
            time.sleep(1)
            
            # Additional fallback using ActionChains
            if select.first_selected_option.text != "Alabama":
                actions = ActionChains(driver)
                actions.move_to_element(dropdown1).click().send_keys("Alabama").send_keys(Keys.ENTER).perform()
                time.sleep(1)
            
            print("Selected Alabama from dropdown")
            print(f"Currently selected option: {select.first_selected_option.text}")
            
        except Exception as e:
            print(f"Error handling dropdown: {str(e)}")
            driver.save_screenshot("dropdown_error.png")

      
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
        time.sleep(5)
        return {"status": "Success", "confirmation": "Form submitted"}

    except Exception as e:
        print(f"Error in form handling: {str(e)}")
        driver.save_screenshot("error_main.png")
        return {"status": "Failed", "error": str(e)}


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
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div[1]/div/div/div/div/div/div/div"
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
   

def handle_brookhavenga_form(driver, url):
  
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
        #checkbox
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[9]/div[1]/div/div/div/div/div/div/div"
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
    
def handle_duluthga_form(driver, url):
   
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
             "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[3]/div[1]/input": form_data["date"],
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[1]/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")

         # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Only to review / inspect")  # Adjust text as per available options
        print("Selected dropdown option")
       
        #checkbox
        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[2]/div[1]/div/div/div/div/div/div/div"
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
  
def handle_norcrossga_form(driver, url):
   
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[4]/div/div[1]/input": form_data["person represented"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[7]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["date"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["time"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/input": form_data["address"],
             "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[16]/div/div[1]/input": form_data["case number"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[20]/div/div[1]/textarea"
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

        # Handle dropdown selection
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[19]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Yes")  # Adjust text as per available options
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
  

def handle_lilburnga_form(driver, url):

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        # Wait for page to load completely
        time.sleep(7)

        # Fill all fields
        fields_to_fill = {
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[6]/div/div[1]/input": form_data["date"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[8]/div/div[1]/input": form_data["name"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[10]/div/div[1]/input": form_data["phone"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[11]/div/div[1]/input": form_data["email"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[12]/div/div[1]/input": form_data["address"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[13]/div/div[1]/input": form_data["city"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[14]/div/div[1]/input": form_data["state"],
            "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[15]/div/div[1]/input": form_data["zip"]
        }

        for xpath, value in fields_to_fill.items():
            fill_field(driver, wait, xpath, value)

        # Fill request details
        details_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[5]/div/div[1]/textarea"
        details = wait.until(EC.presence_of_element_located((By.XPATH, details_xpath)))
        details.clear()
        details.send_keys(form_data["message"])
        print("Filled request details")
        
        dropdown1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[16]/div/div[1]/select"
        dropdown1 = Select(wait.until(EC.presence_of_element_located((By.XPATH, dropdown1_xpath))))
        available_options = [o.text.strip() for o in dropdown1.options]
        print("Available options in dropdown:", available_options)
        dropdown1.select_by_visible_text("Download Digitally")  # Adjust text as per available options
        print("Selected dropdown option")

        checkbox1_xpath = "/html/body/div[1]/div[2]/main/div/div[1]/form/div[2]/div/div[20]/div/div[1]/div/div/div/div/div/div/div"
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
  
def save_results(results, filename="submission_results.csv"):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['url', 'status', 'confirmation', 'error'])
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")


if __name__ == "__main__":
    # Corrected WebDriver initialization
    #service = Service(executable_path='chromedriver.exe')  # Replace with your WebDriver path
    #driver = webdriver.Chrome(service=service)
    driver = create_driver() 
    results = []

    # List of URLs for the forms
    urls = [
        "https://tuckerga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",  # Replace with the actual URL for Tucker form
        "https://forestparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://austellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://acworthga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
         "https://doravillega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
          "https://albanyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://riverdalega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://cityofmorrowga.nextrequest.com/requests/new",
        "https://kennesawga.justfoia.com/Forms/Launch/a3570e65-d44d-43d3-a822-d38e2fc1c3d3",
        "https://smyrnaga.justfoia.com/Forms/Launch/fd208f47-7557-4edf-9478-723c87ba6b30",
        "https://tyronega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://forsythcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://collegeparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://powderspringsga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://conyersga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://spaldingcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://stockbridgega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://stockbridgega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://cityofstonecrestga.nextrequest.com/requests/new",
        "https://peachtreecitygapolice.nextrequest.com/requests/new",
        "https://cityofclarkstonga.nextrequest.com/requests/new",
        "https://cantonga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://maconbibbcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://cherokeecountyga.nextrequest.com/requests/new",
        "https://cityofaugustaga.nextrequest.com/requests/new",
        "https://woodstockga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://eastpointga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://fairburnga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://hapevillega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://brookhavenga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://duluthga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://norcrossga.justfoia.com/Forms/Launch/2da76d30-7849-4d56-b182-ef68865e40f6",
        "https://lilburnga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://www.cityofgriffin.com/services/open-records"
    ]

    for url in urls:
        if url == "https://tuckerga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_tucker_form(driver, url)
        elif url == "https://forestparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_forestparkga_form(driver, url)
        elif url == "https://austellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_austellga_form(driver, url)
        elif url == "https://acworthga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_acworthga_form(driver, url)
        elif url == "https://doravillega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_doravillega_form(driver, url)
        elif url == "https://albanyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_albanyga_form(driver, url)
        elif url == "https://riverdalega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_riverdalega_form(driver, url)
        elif url == "https://cityofmorrowga.nextrequest.com/requests/new":
            result = handle_cityofmorrowga_form(driver, url)
        elif url == "https://kennesawga.justfoia.com/Forms/Launch/a3570e65-d44d-43d3-a822-d38e2fc1c3d3":
            result = handle_kennesawga_form(driver, url)
        elif url == "https://smyrnaga.justfoia.com/Forms/Launch/fd208f47-7557-4edf-9478-723c87ba6b30":
            result = handle_smyrnaga_form(driver, url)
        elif url == "https://tyronega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_tyronega_form(driver, url)
        elif url == "https://forsythcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_forsythcountyga_form(driver, url)
        elif url == "https://collegeparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_collegeparkga_form(driver, url)
        elif url == "https://powderspringsga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_powderspringsga_form(driver, url)
        elif url == "https://conyersga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_conyersga_form(driver, url)
        elif url == "https://spaldingcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_spaldingcountyga_form(driver, url)
        elif url == "https://stockbridgega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_stockbridgega_form(driver, url)
        elif url == "https://cityofstonecrestga.nextrequest.com/requests/new":
            result = handle_cityofstonecrestga_form(driver, url)
        elif url == "https://peachtreecitygapolice.nextrequest.com/requests/new":
            result = handle_peachtreecitygapolice_form(driver, url)
        elif url == "https://cityofclarkstonga.nextrequest.com/requests/new":
            result = handle_cityofclarkstonga_form(driver, url)
        elif url == "https://cantonga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_cantonga_form(driver, url)
        elif url == "https://maconbibbcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_maconbibbcountyga_form(driver, url)
        elif url == "https://cherokeecountyga.nextrequest.com/requests/new":
            result = handle_cherokeecountyga_form(driver, url)
        elif url == "https://cityofaugustaga.nextrequest.com/requests/new":
            result = handle_cityofaugustaga_form(driver, url)
        elif url == "https://woodstockga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_woodstockga_form(driver, url)
        elif url == "https://eastpointga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_eastpointga_form(driver, url)
        elif url == "https://fairburnga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_fairburnga_form(driver, url)
        elif url == "https://hapevillega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_hapevillega_form(driver, url)
        elif url == "https://brookhavenga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_brookhavenga_form(driver, url)
        elif url == "https://duluthga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_duluthga_form(driver, url)
        elif url == "https://norcrossga.justfoia.com/Forms/Launch/2da76d30-7849-4d56-b182-ef68865e40f6":
            result = handle_norcrossga_form(driver, url)
        elif url == "https://lilburnga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_lilburnga_form(driver, url)
        elif url == "https://www.cityofgriffin.com/services/open-records":
            result = handle_cityofgriffin_form(driver, url)
        results.append({"url": url, "status": result["status"], "confirmation": result.get("confirmation", ""), "error": result.get("error", "")})

    # Save results
    save_results(results)

    # Close the driver
    driver.quit()
    

