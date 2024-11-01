import unittest

import self
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

    def fill_fill_description(self, initial_deposit):
        """Fill in the initial deposit."""
        self.driver.find_element(By.NAME, "desc").send_keys(initial_deposit)

    def trigger_validation(self):
        """Trigger validation by moving focus away."""
        self.driver.find_element(By.NAME, "inideposit").send_keys(Keys.TAB)  # Move focus away

    def check_error_message(self, expected_message, message_id):
        """Check for the expected error message."""
        error_msg = self.wait.until(EC.visibility_of_element_located((By.ID, message_id)))
        actual_message = error_msg.text.strip()
        self.assertEqual(actual_message, expected_message, f"Error message is incorrect: expected '{expected_message}', got '{actual_message}'!")

    # Test cases

    # 1. Account No là bắt buộc
    def test_customer_id_is_required(self):
        self.click_new_account_link()
        self.fill_customer_id("")  # Leave blank
        self.trigger_validation()
        self.check_error_message("Customer ID is required", "message14")
        self.reset_form()

    # 2. Amount là bắt buộc
    def test_initial_deposit_is_required(self):
        self.click_new_account_link()
        self.fill_initial_deposit("")  # Leave blank
        self.trigger_validation()
        self.check_error_message("Initial Deposit must not be blank", "message19")
        self.reset_form()

    # 3. Description là bắt buộc
    def test_description_is_required(self):
        self.click_new_account_link()
        self.fill_description("")  # Leave blank
        self.trigger_validation()
        self.check_error_message("Description can not be blank", "message17")
        self.reset_form()

    # 4. Account No không cho phép ký tự
    def test_customer_id_cannot_have_characters(self):
        self.click_new_account_link()
        self.fill_customer_id("abcd1234")  # Invalid characters
        self.trigger_validation()
        self.check_error_message("Characters are not allowed", "message14")
        self.reset_form()

    # 5. Amount không cho phép ký tự
    def test_initial_deposit_cannot_have_characters(self):
        self.click_new_account_link()
        self.fill_initial_deposit("abcd1234")  # Invalid characters
        self.trigger_validation()
        self.check_error_message("Characters are not allowed", "message19")
        self.reset_form()

    # 7. Account No không cho phép ký tự đặc biệt
    def test_customer_id_cannot_have_special_characters(self):
        self.click_new_account_link()
        self.fill_customer_id("!@#$%")  # Special characters
        self.trigger_validation()
        self.check_error_message("Special characters are not allowed", "message14")
        self.reset_form()

    # 8. Amount không cho phép ký tự đặc biệt
    def test_initial_deposit_cannot_have_special_characters(self):
        self.click_new_account_link()
        self.fill_initial_deposit("!@#$%")  # Special characters
        self.trigger_validation()
        self.check_error_message("Special characters are not allowed", "message19")
        self.reset_form()

#Nhập đúng tất cả các trường
    def test_deposit_successful(self):
        self.click_new_account_link()
        self.fill_customer_id("12345")
        self.fill_amount("7000")
        self.fill_description("abc")
        # Click the submit button
        self.submit_form()

        # Check if the success dialog is displayed
        success_dialog = self.wait.until(EC.presence_of_element_located((By.ID, "success_dialog")))
        self.assertTrue(success_dialog.is_displayed())
        self.assertEqual(success_dialog.text, "Deposit successful")

        # Close the success dialog
        close_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#success_dialog button.close")))
        close_button.click()

    # Nhập Tài khoản không tồn tại
    def test_successful_deposit(self):
        self.click_new_account_link()
        self.fill_customer_id("12345")
        self.fill_initial_deposit("7000")
        self.fill_description("abc")
        self.submit_form()

        # Check if the page navigates to the expected URL
        current_url = self.driver.current_url
        self.assertIn("https://www.demo.guru99.com/V4/manager/Deposit.php", current_url,
                      "Account does not exist")

        self.check_success_dialog()



    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)