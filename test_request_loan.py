"""
Automated Testing Script for Parabank - Request Loan
Test Cases: TC_LOAN_01 to TC_LOAN_07
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

class TestRequestLoan:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.screenshot_dir = "screenshots/request_loan"
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def create_driver(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        return driver, wait

    def take_screenshot(self, driver, name):
        filepath = f"{self.screenshot_dir}/{name}.png"
        driver.save_screenshot(filepath)
        print(f"    [Screenshot] Saved: {filepath}")
        return filepath

    def login(self, driver, wait):
        driver.get("https://parabank.parasoft.com")
        time.sleep(2)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_field.send_keys("john")
        driver.find_element(By.NAME, "password").send_keys("demo")
        driver.find_element(By.XPATH, "//input[@value='Log In']").click()
        time.sleep(2)

    def test_loan_page_access(self):
        print("\n=== TC_LOAN_01: Request Loan Page Access ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            loan_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Request Loan")))
            loan_link.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_LOAN_01_01_loan_page")

            # Check required fields
            try:
                driver.find_element(By.ID, "amount")
                driver.find_element(By.ID, "downPayment")
                driver.find_element(By.ID, "fromAccountId")
                print("[PASS] PASS: Loan request page loaded with all fields")
                self.passed += 1
            except:
                print("[FAIL] FAIL: Required loan fields missing")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOAN_01_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_valid_loan_request(self):
        print("\n=== TC_LOAN_02: Valid Loan Request ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/requestloan.htm")
            time.sleep(2)

            driver.find_element(By.ID, "amount").send_keys("1000")
            driver.find_element(By.ID, "downPayment").send_keys("100")

            self.take_screenshot(driver, "TC_LOAN_02_01_form_filled")

            apply_button = driver.find_element(By.XPATH, "//input[@value='Apply Now']")
            apply_button.click()
            time.sleep(3)

            self.take_screenshot(driver, "TC_LOAN_02_02_result")

            page_source = driver.page_source.lower()
            if "approved" in page_source or "denied" in page_source:
                print("[PASS] PASS: Loan request processed successfully")
                self.passed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error during loan request")
                self.failed += 1
            else:
                print("[FAIL] FAIL: No loan response received")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOAN_02_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_zero_down_payment(self):
        print("\n=== TC_LOAN_03: Zero Down Payment ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/requestloan.htm")
            time.sleep(2)

            driver.find_element(By.ID, "amount").send_keys("5000")
            driver.find_element(By.ID, "downPayment").send_keys("0")

            self.take_screenshot(driver, "TC_LOAN_03_01_zero_downpayment")

            apply_button = driver.find_element(By.XPATH, "//input[@value='Apply Now']")
            apply_button.click()
            time.sleep(3)

            self.take_screenshot(driver, "TC_LOAN_03_02_result")

            page_source = driver.page_source.lower()
            if "approved" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Loan APPROVED with ZERO down payment (should require down payment)")
                self.failed += 1
            elif "denied" in page_source:
                print("[PASS] PASS: Loan correctly denied for zero down payment")
                self.passed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Internal server error")
                self.failed += 1
            else:
                print("[PASS] PASS: Zero down payment handled appropriately")
                self.passed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOAN_03_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_loan_amount(self):
        print("\n=== TC_LOAN_04: Empty Loan Amount Validation ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/requestloan.htm")
            time.sleep(2)

            # Only fill down payment
            driver.find_element(By.ID, "downPayment").send_keys("100")

            self.take_screenshot(driver, "TC_LOAN_04_01_empty_amount")

            apply_button = driver.find_element(By.XPATH, "//input[@value='Apply Now']")
            apply_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_LOAN_04_02_result")

            page_source = driver.page_source.lower()
            if "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG - Internal server error instead of proper validation for empty amount")
                self.failed += 1
            elif "approved" in page_source or "denied" in page_source:
                print("[FAIL] FAIL: BUG - Loan processed with empty amount field (should show validation)")
                self.failed += 1
            else:
                # Page stayed on form or showed validation - correct behavior
                print("[PASS] PASS: Empty loan amount not processed (validation working)")
                self.passed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOAN_04_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_negative_loan_amount(self):
        print("\n=== TC_LOAN_05: Negative Loan Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/requestloan.htm")
            time.sleep(2)

            driver.find_element(By.ID, "amount").send_keys("-5000")
            driver.find_element(By.ID, "downPayment").send_keys("100")

            self.take_screenshot(driver, "TC_LOAN_05_01_negative_amount")

            apply_button = driver.find_element(By.XPATH, "//input[@value='Apply Now']")
            apply_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_LOAN_05_02_result")

            page_source = driver.page_source.lower()
            if "approved" in page_source:
                print("[FAIL] FAIL: BUG - System approved negative loan amount")
                self.failed += 1
            elif "denied" in page_source:
                print("[PASS] PASS: Negative loan amount correctly denied")
                self.passed += 1
            elif "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error for negative loan amount")
                self.failed += 1
            else:
                print("[PASS] PASS: Negative loan amount rejected")
                self.passed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOAN_05_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_extremely_large_loan(self):
        print("\n=== TC_LOAN_06: Extremely Large Loan Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/requestloan.htm")
            time.sleep(2)

            driver.find_element(By.ID, "amount").send_keys("999999999999")
            driver.find_element(By.ID, "downPayment").send_keys("100")

            self.take_screenshot(driver, "TC_LOAN_06_01_huge_amount")

            apply_button = driver.find_element(By.XPATH, "//input[@value='Apply Now']")
            apply_button.click()
            time.sleep(3)

            self.take_screenshot(driver, "TC_LOAN_06_02_result")

            page_source = driver.page_source.lower()
            if "approved" in page_source or "denied" in page_source:
                print("[PASS] PASS: Large loan amount properly handled")
                self.passed += 1
            elif "an internal error has occurred" in page_source or "exception" in page_source or "overflow" in page_source:
                print("[FAIL] FAIL: BUG FOUND - System crashed on large loan amount")
                self.failed += 1
            else:
                print("[PASS] PASS: System handled large loan request")
                self.passed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOAN_06_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_special_chars_in_amount(self):
        print("\n=== TC_LOAN_07: Special Characters in Amount (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/requestloan.htm")
            time.sleep(2)

            driver.find_element(By.ID, "amount").send_keys("1000<script>alert(1)</script>")
            driver.find_element(By.ID, "downPayment").send_keys("100")

            self.take_screenshot(driver, "TC_LOAN_07_01_special_chars")

            apply_button = driver.find_element(By.XPATH, "//input[@value='Apply Now']")
            apply_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_LOAN_07_02_result")

            try:
                alert = driver.switch_to.alert
                print("[FAIL] FAIL: XSS vulnerability detected")
                alert.accept()
                self.failed += 1
            except:
                print("[PASS] PASS: Special characters handled safely")
                self.passed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_LOAN_07_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK REQUEST LOAN TEST SUITE")
        print("="*60)

        self.test_loan_page_access()
        self.test_valid_loan_request()
        self.test_zero_down_payment()
        self.test_empty_loan_amount()
        self.test_negative_loan_amount()
        self.test_extremely_large_loan()
        self.test_special_chars_in_amount()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("REQUEST LOAN TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}


if __name__ == "__main__":
    test_suite = TestRequestLoan()
    test_suite.run_all_tests()