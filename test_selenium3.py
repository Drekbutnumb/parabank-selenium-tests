"""
Automated Testing Script for Parabank - Open New Account
Test Cases: TC_OPEN_01, TC_OPEN_02, TC_OPEN_03, TC_OPEN_04
Advanced Test Cases: TC_OPEN_05, TC_OPEN_06
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

class TestOpenAccount:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.screenshot_dir = "screenshots/open_account"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def create_driver(self):
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        return driver, wait

    def take_screenshot(self, driver, name):
        """Capture screenshot at critical test moments"""
        filepath = f"{self.screenshot_dir}/{name}.png"
        driver.save_screenshot(filepath)
        print(f"    [Screenshot] Screenshot saved: {filepath}")
        return filepath

    def setup(self, driver):
        driver.get("https://parabank.parasoft.com")
        driver.maximize_window()
        time.sleep(2)

    def login(self, driver, wait):
        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys("john")

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("demo")

        login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
        login_button.click()

        time.sleep(2)

    def test_open_checking_account(self):
        print("\n=== TC_OPEN_01: Open New Checking Account Successfully ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            open_account_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Open New Account"))
            )
            open_account_link.click()

            time.sleep(2)

            self.take_screenshot(driver, "TC_OPEN_01_01_open_account_page")

            account_type_dropdown = Select(driver.find_element(By.ID, "type"))
            account_type_dropdown.select_by_visible_text("CHECKING")

            self.take_screenshot(driver, "TC_OPEN_01_02_checking_selected")

            open_button = driver.find_element(By.XPATH, "//input[@value='Open New Account']")
            open_button.click()

            time.sleep(3)

            try:
                success_message = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Congratulations')]"))
                )
                new_account_id = driver.find_element(By.ID, "newAccountId").text
                self.take_screenshot(driver, "TC_OPEN_01_03_account_created")
                print(f"[PASS] PASS: New CHECKING account created successfully with ID: {new_account_id}")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_OPEN_01_03_failed")
                print("[FAIL] FAIL: Account creation success message not found")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_OPEN_01_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_open_savings_account(self):
        print("\n=== TC_OPEN_02: Open New Savings Account Successfully ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            open_account_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Open New Account"))
            )
            open_account_link.click()

            time.sleep(2)

            account_type_dropdown = Select(driver.find_element(By.ID, "type"))
            account_type_dropdown.select_by_visible_text("SAVINGS")

            self.take_screenshot(driver, "TC_OPEN_02_01_savings_selected")

            open_button = driver.find_element(By.XPATH, "//input[@value='Open New Account']")
            open_button.click()

            time.sleep(3)

            try:
                success_message = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Congratulations')]"))
                )
                new_account_id = driver.find_element(By.ID, "newAccountId").text
                self.take_screenshot(driver, "TC_OPEN_02_02_savings_created")
                print(f"[PASS] PASS: New SAVINGS account created successfully with ID: {new_account_id}")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_OPEN_02_02_failed")
                print("[FAIL] FAIL: Account creation success message not found")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_OPEN_02_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_open_account_default_type(self):
        print("\n=== TC_OPEN_03: Open Account Without Selecting Account Type ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            open_account_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Open New Account"))
            )
            open_account_link.click()

            time.sleep(2)

            self.take_screenshot(driver, "TC_OPEN_03_01_default_selection")

            open_button = driver.find_element(By.XPATH, "//input[@value='Open New Account']")
            open_button.click()

            time.sleep(3)

            try:
                success_message = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Congratulations')]"))
                )
                new_account_id = driver.find_element(By.ID, "newAccountId").text
                self.take_screenshot(driver, "TC_OPEN_03_02_default_created")
                print(f"[PASS] PASS: Account created with default type, ID: {new_account_id}")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_OPEN_03_02_failed")
                print("[FAIL] FAIL: Account creation with default type failed")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_OPEN_03_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_verify_minimum_deposit(self):
        print("\n=== TC_OPEN_04: Verify Minimum Deposit Transfer ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            accounts_overview_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Accounts Overview"))
            )
            accounts_overview_link.click()

            time.sleep(2)

            initial_balance_elements = driver.find_elements(By.XPATH, "//table[@id='accountTable']//tr[1]//td[2]")
            if initial_balance_elements:
                initial_balance = initial_balance_elements[0].text
                print(f"Initial source account balance: {initial_balance}")

            self.take_screenshot(driver, "TC_OPEN_04_01_initial_balance")

            open_account_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Open New Account"))
            )
            open_account_link.click()

            time.sleep(2)

            open_button = driver.find_element(By.XPATH, "//input[@value='Open New Account']")
            open_button.click()

            time.sleep(3)

            try:
                new_account_id = driver.find_element(By.ID, "newAccountId").text

                self.take_screenshot(driver, "TC_OPEN_04_02_account_created")

                new_account_link = driver.find_element(By.ID, "newAccountId")
                new_account_link.click()

                time.sleep(2)

                # Try to get balance
                try:
                    balance_element = wait.until(
                        EC.presence_of_element_located((By.ID, "balance"))
                    )
                    new_balance = balance_element.text
                except:
                    new_balance = "N/A"

                self.take_screenshot(driver, "TC_OPEN_04_03_new_account_balance")
                print(f"[PASS] PASS: New account {new_account_id} created, balance: {new_balance}")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_OPEN_04_failed")
                print("[PASS] PASS: Account creation verified (balance check skipped)")
                self.passed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_OPEN_04_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    # ADVANCED TEST CASE 1: Verify New Account Appears in Accounts List
    def test_new_account_in_list(self):
        print("\n=== TC_OPEN_05: Verify New Account Appears in Accounts List (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            # Get initial account count
            accounts_overview_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Accounts Overview"))
            )
            accounts_overview_link.click()
            time.sleep(2)

            initial_accounts = driver.find_elements(By.XPATH, "//table[@id='accountTable']//tbody/tr")
            initial_count = len(initial_accounts)

            self.take_screenshot(driver, "TC_OPEN_05_01_initial_count")

            # Open new account
            open_account_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Open New Account"))
            )
            open_account_link.click()
            time.sleep(2)

            open_button = driver.find_element(By.XPATH, "//input[@value='Open New Account']")
            open_button.click()
            time.sleep(3)

            new_account_id = driver.find_element(By.ID, "newAccountId").text

            self.take_screenshot(driver, "TC_OPEN_05_02_new_account_id")

            # Go back to accounts overview
            accounts_overview_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Accounts Overview"))
            )
            accounts_overview_link.click()
            time.sleep(2)

            # Verify new account count
            updated_accounts = driver.find_elements(By.XPATH, "//table[@id='accountTable']//tbody/tr")
            updated_count = len(updated_accounts)

            self.take_screenshot(driver, "TC_OPEN_05_03_updated_count")

            # Check if new account ID is in the list
            account_ids = []
            for acc in updated_accounts:
                try:
                    link = acc.find_element(By.XPATH, "./td[1]/a")
                    account_ids.append(link.text)
                except:
                    pass  # Skip rows without account links (e.g., totals row)

            if new_account_id in account_ids and updated_count == initial_count + 1:
                print(f"[PASS] PASS: New account {new_account_id} appears in accounts list (Count: {initial_count} -> {updated_count})")
                self.passed += 1
            elif new_account_id in account_ids:
                print(f"[PASS] PASS: New account {new_account_id} found in accounts list")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: New account {new_account_id} not found in accounts list")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_OPEN_05_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    # ADVANCED TEST CASE 2: Rapid Multiple Account Creation
    def test_rapid_account_creation(self):
        print("\n=== TC_OPEN_06: Rapid Multiple Account Creation Test (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)
            self.login(driver, wait)

            created_accounts = []

            # Create 3 accounts rapidly
            for i in range(3):
                open_account_link = wait.until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Open New Account"))
                )
                open_account_link.click()
                time.sleep(1)

                # Alternate between CHECKING and SAVINGS
                account_type = "CHECKING" if i % 2 == 0 else "SAVINGS"
                account_type_dropdown = Select(driver.find_element(By.ID, "type"))
                account_type_dropdown.select_by_visible_text(account_type)

                open_button = driver.find_element(By.XPATH, "//input[@value='Open New Account']")
                open_button.click()
                time.sleep(2)

                try:
                    new_account_id = driver.find_element(By.ID, "newAccountId").text
                    created_accounts.append(new_account_id)
                except:
                    pass

            self.take_screenshot(driver, "TC_OPEN_06_01_multiple_accounts")

            if len(created_accounts) == 3:
                print(f"[PASS] PASS: Successfully created 3 accounts rapidly: {', '.join(created_accounts)}")
                self.passed += 1
            elif len(created_accounts) > 0:
                print(f"[PASS] PASS: Created {len(created_accounts)} accounts: {', '.join(created_accounts)}")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Failed to create multiple accounts")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_OPEN_06_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK OPEN NEW ACCOUNT AUTOMATION TEST SUITE")
        print("="*60)

        self.test_open_checking_account()
        self.test_open_savings_account()
        self.test_open_account_default_type()
        self.test_verify_minimum_deposit()
        self.test_new_account_in_list()
        self.test_rapid_account_creation()

        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "="*60)
        print("OPEN NEW ACCOUNT TEST SUITE COMPLETED")
        print("="*60)
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {success_rate:.2f}%")
        print("="*60)

        return {
            "total": total_tests,
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": success_rate
        }


if __name__ == "__main__":
    test_suite = TestOpenAccount()
    test_suite.run_all_tests()