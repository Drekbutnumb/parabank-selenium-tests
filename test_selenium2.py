"""
Automated Testing Script for Parabank - User Login
Test Cases: TC_LOGIN_01, TC_LOGIN_02, TC_LOGIN_03, TC_LOGIN_04, TC_LOGIN_05
Advanced Test Cases: TC_LOGIN_06, TC_LOGIN_07
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestLogin:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.screenshot_dir = "screenshots/login"
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
        print(f"    📸 Screenshot saved: {filepath}")
        return filepath

    def setup(self, driver):
        driver.get("https://parabank.parasoft.com")
        driver.maximize_window()
        time.sleep(2)

    def test_valid_login(self):
        print("\n=== TC_LOGIN_01: Valid Login Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            self.take_screenshot(driver, "TC_LOGIN_01_01_login_page")

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("john")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("demo")

            self.take_screenshot(driver, "TC_LOGIN_01_02_credentials_entered")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            try:
                accounts_overview = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accounts Overview')]"))
                )
                self.take_screenshot(driver, "TC_LOGIN_01_03_login_success")
                print("✓ PASS: User logged in successfully, Accounts Overview page displayed")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_LOGIN_01_03_login_failed")
                print("✗ FAIL: Login failed or Accounts Overview page not displayed")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOGIN_01_error")
            print(f"✗ FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_username(self):
        print("\n=== TC_LOGIN_02: Invalid Username Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("invaliduser999")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("demo")

            self.take_screenshot(driver, "TC_LOGIN_02_01_invalid_username_entered")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            try:
                error_message = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                self.take_screenshot(driver, "TC_LOGIN_02_02_error_displayed")
                print("✓ PASS: Error message displayed for invalid username")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_LOGIN_02_02_result")
                print("✗ FAIL: No error message displayed for invalid username")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOGIN_02_error")
            print(f"✗ FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_password(self):
        print("\n=== TC_LOGIN_03: Invalid Password Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("john")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("wrongpassword123")

            self.take_screenshot(driver, "TC_LOGIN_03_01_invalid_password_entered")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            try:
                error_message = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                self.take_screenshot(driver, "TC_LOGIN_03_02_error_displayed")
                print("✓ PASS: Error message displayed for invalid password")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_LOGIN_03_02_result")
                print("✗ FAIL: No error message displayed for invalid password")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOGIN_03_error")
            print(f"✗ FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_credentials(self):
        print("\n=== TC_LOGIN_04: Empty Username and Password Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            self.take_screenshot(driver, "TC_LOGIN_04_01_empty_fields")

            login_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@value='Log In']"))
            )
            login_button.click()

            time.sleep(2)

            try:
                error_message = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                self.take_screenshot(driver, "TC_LOGIN_04_02_error_displayed")
                print("✓ PASS: Error message displayed for empty credentials")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_LOGIN_04_02_result")
                print("✗ FAIL: No error message displayed for empty credentials")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOGIN_04_error")
            print(f"✗ FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_password(self):
        print("\n=== TC_LOGIN_05: Empty Password Only Test ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("john")

            self.take_screenshot(driver, "TC_LOGIN_05_01_username_only")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            try:
                error_message = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                self.take_screenshot(driver, "TC_LOGIN_05_02_error_displayed")
                print("✓ PASS: Error message displayed for empty password")
                self.passed += 1
            except:
                self.take_screenshot(driver, "TC_LOGIN_05_02_result")
                print("✗ FAIL: No error message displayed for empty password")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOGIN_05_error")
            print(f"✗ FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    # ADVANCED TEST CASE 1: SQL Injection Prevention Test
    def test_sql_injection_prevention(self):
        print("\n=== TC_LOGIN_06: SQL Injection Prevention Test (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            # SQL injection payload
            sql_injection = "' OR '1'='1"

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(sql_injection)

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys(sql_injection)

            self.take_screenshot(driver, "TC_LOGIN_06_01_sql_injection_attempt")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            self.take_screenshot(driver, "TC_LOGIN_06_02_result")

            # Check if login was blocked (no unauthorized access)
            page_source_lower = driver.page_source.lower()
            if "accounts overview" not in page_source_lower and "sql" not in page_source_lower:
                print("✓ PASS: SQL injection attempt blocked - no unauthorized access")
                self.passed += 1
            elif "error" in page_source_lower:
                print("✓ PASS: SQL injection attempt handled safely with error message")
                self.passed += 1
            else:
                print("✗ FAIL: Potential SQL injection vulnerability")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOGIN_06_error")
            print(f"✗ FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    # ADVANCED TEST CASE 2: Session Management After Logout
    def test_session_management_after_logout(self):
        print("\n=== TC_LOGIN_07: Session Management After Logout (ADVANCED) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.setup(driver)

            # First, login successfully
            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys("john")

            password_field = driver.find_element(By.NAME, "password")
            password_field.send_keys("demo")

            login_button = driver.find_element(By.XPATH, "//input[@value='Log In']")
            login_button.click()

            time.sleep(2)

            # Verify login success
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Accounts Overview')]"))
            )

            self.take_screenshot(driver, "TC_LOGIN_07_01_logged_in")

            # Logout
            logout_link = wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Log Out"))
            )
            logout_link.click()

            time.sleep(2)

            self.take_screenshot(driver, "TC_LOGIN_07_02_after_logout")

            # Try to access protected page directly (more reliable than back button)
            driver.get("https://parabank.parasoft.com/parabank/overview.htm")
            time.sleep(2)

            self.take_screenshot(driver, "TC_LOGIN_07_03_direct_access_attempt")

            # Verify session is invalidated - should see login form or error, not account data
            page_source = driver.page_source.lower()

            # Check if login form is present (properly logged out)
            login_form_present = False
            try:
                driver.find_element(By.NAME, "username")
                login_form_present = True
            except:
                pass

            # Check if there's an error message about not being logged in
            error_present = "error" in page_source or "please login" in page_source or "log in" in page_source

            if login_form_present or error_present:
                print("✓ PASS: Session properly invalidated after logout - access denied")
                self.passed += 1
            else:
                print("✗ FAIL: Session not properly invalidated - protected data still accessible")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOGIN_07_error")
            print(f"✗ FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK LOGIN AUTOMATION TEST SUITE")
        print("="*60)

        self.test_valid_login()
        self.test_invalid_username()
        self.test_invalid_password()
        self.test_empty_credentials()
        self.test_empty_password()
        self.test_sql_injection_prevention()
        self.test_session_management_after_logout()

        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0

        print("\n" + "="*60)
        print("LOGIN TEST SUITE COMPLETED")
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
    test_suite = TestLogin()
    test_suite.run_all_tests()