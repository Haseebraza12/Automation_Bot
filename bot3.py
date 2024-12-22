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
    "email": "dummyemail@example.com",
    "address": "123 Main Street, Suite 100",
    "city": "SampleCity",
    "state": "SampleState",
    "zip": "12345",
    "company":"no",
    "message": """My name is John Doe, and I am requesting records from the Code Enforcement Office.

In accordance with the [Insert Local Open Records Act], I am requesting a list of all open code violations for residential properties over the past 30 days. Specifically, I am interested in violations related to damaged or decayed roofs, mold, broken windows, boarded-up windows and doors, overgrown weeds and grass, trash and debris, rodent infestations or unsanitary conditions, flaking or peeling paint, vacant and unsecured structures, and any buildings deemed dangerous, uninhabitable, or unfit for occupancy.

Please provide the details of these violations, including the nature of the violation, the address of the property, and the date of the violation. If possible, I would appreciate receiving the information in a digital format, such as a .csv file or a searchable PDF. However, I am happy to accept the information in any format that is convenient for your office.

Thank you for your assistance in this matter.

Sincerely,
John Doe"""
}

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


def save_results(results, filename="submission3_results.csv"):
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
    service = Service(executable_path='C:/Users/Haseeb Raza/Desktop/BOT/chromedriver.exe')  # Replace with your WebDriver path
    driver = webdriver.Chrome(service=service)
    results = []

    # List of URLs for the forms
    urls = [
        "https://cherokeecountyga.nextrequest.com/requests/new",
        "https://albanyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://collegeparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://cityofaugustaga.nextrequest.com/requests/new",
        "https://cityoffayettevillega.nextrequest.com/requests/new",
        "https://peachtreecitygapolice.nextrequest.com/requests/new",
        "https://unioncityga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://maconbibbcountyga.justfoia.com/Forms/Launch/a709d888-de2f-4857-9c82-b12b2645a87c",
        "https://cantonga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://hapevillega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://fairburnga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://eastpointga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://woodstockga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://spaldingcountyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
        "https://riverdalega.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
         "https://acworthga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
         "https://austellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
         "https://forestparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
         "https://roswellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",
         "https://conyersga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb",




        

    ]

    for url in urls:
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
        elif url == "https://albanyga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_albanyga_form(driver, url)
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
        elif url ==  "https://acworthga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_acworthga_form(driver, url)
        elif url == "https://austellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_austellga_form(driver, url)
        elif url == "https://forestparkga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_forestparkga_form(driver, url)
        elif url == "https://roswellga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_roswellga_form(driver, url)
        elif url == "https://conyersga.justfoia.com/Forms/Launch/d705cbd6-1396-49b7-939e-8d86c5a87deb":
            result = handle_conyersga_form(driver, url)
        results.append({"url": url, "status": result["status"], "confirmation": result.get("confirmation", ""), "error": result.get("error", "")})

    # Save results
    save_results(results)

    # Close the driver
    driver.quit()
    

