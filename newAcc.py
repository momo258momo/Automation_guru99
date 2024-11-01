import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FundTransferTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.credentials = {
            "username": "mngr599452",
            "password": "pEtUmeh",
            "login_url": "https://www.demo.guru99.com/V4"
        }
        self.driver.get(self.credentials["login_url"])
        self.login()
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        """Log in to the application."""
        self.driver.find_element(By.NAME, "uid").send_keys(self.credentials["username"])
        self.driver.find_element(By.NAME, "password").send_keys(self.credentials["password"])
        self.driver.find_element(By.NAME, "btnLogin").click()

    def reset_form(self):
        """Reset the form to clear all fields."""
        reset_button = self.wait.until(
            EC.element_to_be_clickable((By.NAME, "reset"))
        )
        reset_button.click()

    def click_new_account_link(self):
        """Click the 'New Account' link."""
        new_account_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "New Account"))
        )
        new_account_link.click()

    def fill_customer_id(self, customer_id):
        """Fill in the customer ID."""
        self.driver.find_element(By.NAME, "cusid").send_keys(customer_id)

    def fill_initial_deposit(self, initial_deposit):
        """Fill in the initial deposit."""
        self.driver.find_element(By.NAME, "inideposit").send_keys(initial_deposit)

    def submit_form(self):
        """Submit the form."""
        self.driver.find_element(By.NAME, "button2").click()

    def trigger_validation(self):
        """Trigger validation by moving focus away."""
        self.driver.find_element(By.NAME, "inideposit").send_keys(Keys.TAB)  # Move focus away

    def check_error_message(self, expected_message, message_id):
        """Check for the expected error message."""
        error_msg = self.wait.until(EC.visibility_of_element_located((By.ID, message_id)))
        self.assertEqual(error_msg.text.strip(), expected_message, f"Error message is incorrect or not displayed!")

    def handle_alert(self):
        """Handle possible alert after form submission."""
        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()  # Dismiss the alert
        except Exception:
            print("No alert was present after form submission.")

    def test_customer_id_is_required(self):
        """Test that Customer ID is required."""
        print("Running test: Customer ID is required")
        self.click_new_account_link()
        self.fill_customer_id("")  # Leave blank
        self.trigger_validation()
        self.check_error_message("Customer ID is required", "message14")
        self.reset_form()
        print("Test passed")

    def test_initial_deposit_is_required(self):
        """Test that Initial Deposit is required."""
        print("Running test: Initial Deposit is required")
        self.click_new_account_link()
        self.fill_customer_id("1234")
        self.fill_initial_deposit("")  # Leave blank
        self.trigger_validation()
        self.check_error_message("Initial Deposit must not be blank", "message19")
        self.reset_form()
        print("Test passed")

    def test_customer_id_cannot_have_characters(self):
        """Test that Customer ID cannot have characters."""
        print("Running test: Customer ID cannot have characters")
        self.click_new_account_link()
        self.fill_customer_id("abc")  # Invalid characters
        self.trigger_validation()
        self.check_error_message("Characters are not allowed", "message14")
        self.reset_form()
        print("Test passed")

    def test_initial_deposit_cannot_have_characters(self):
        """Test that Initial Deposit cannot have characters."""
        print("Running test: Initial Deposit cannot have characters")
        self.click_new_account_link()
        self.fill_customer_id("1234")
        self.fill_initial_deposit("abc")  # Invalid characters
        self.trigger_validation()
        self.check_error_message("Characters are not allowed", "message19")
        self.reset_form()
        print("Test passed")

    def test_customer_id_cannot_have_special_characters(self):
        """Test that Customer ID cannot have special characters."""
        print("Running test: Customer ID cannot have special characters")
        self.click_new_account_link()
        self.fill_customer_id("!@#")  # Special characters
        self.trigger_validation()
        self.check_error_message("Special characters are not allowed", "message14")
        self.reset_form()
        print("Test passed")

    def test_initial_deposit_cannot_have_special_characters(self):
        """Test that Initial Deposit cannot have special characters."""
        print("Running test: Initial Deposit cannot have special characters")
        self.click_new_account_link()
        self.fill_customer_id("1234")
        self.fill_initial_deposit("!@#")  # Special characters
        self.trigger_validation()
        self.check_error_message("Special characters are not allowed", "message19")
        self.reset_form()
        print("Test passed")

    def test_valid_input_creates_account(self):
        """Test creating a new account with valid details."""
        print("Running test: Valid input creates account")
        self.click_new_account_link()
        self.fill_customer_id("1234")
        self.fill_initial_deposit("7000")

        # Select account type
        account_type_select = self.driver.find_element(By.NAME, "selaccount")
        account_type_select.click()
        savings_option = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//option[@value='Savings']"))
        )
        savings_option.click()

        self.submit_form()
        self.handle_alert()

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//h2[contains(text(),'Account Created Successfully')]"))
        )
        current_url = self.driver.current_url
        expected_url = "https://www.demo.guru99.com/V4/manager/insertAccount.php"
        self.assertEqual(current_url, expected_url, "Account creation failed; not redirected correctly.")
        print("Test passed")

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)