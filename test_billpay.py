"""
Automated Testing Script for Parabank - Bill Pay
Test Cases: TC_BILL_01 to TC_BILL_07
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class TestBillPay:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.screenshot_dir = "screenshots/billpay"
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

    def test_billpay_page_access(self):
        print("\n=== TC_BILL_01: Bill Pay Page Access ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            billpay_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Bill Pay")))
            billpay_link.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_BILL_01_01_billpay_page")

            # Check all required fields present
            fields = ["payee.name", "payee.address.street", "payee.address.city",
                     "payee.address.state", "payee.address.zipCode", "payee.phoneNumber",
                     "payee.accountNumber", "verifyAccount", "amount"]

            missing_fields = []
            for field in fields:
                try:
                    driver.find_element(By.NAME, field)
                except:
                    missing_fields.append(field)

            if len(missing_fields) == 0:
                print("[PASS] PASS: All Bill Pay form fields present")
                self.passed += 1
            else:
                print(f"[FAIL] FAIL: Missing fields: {missing_fields}")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_BILL_01_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_valid_bill_payment(self):
        print("\n=== TC_BILL_02: Valid Bill Payment ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            # Fill bill pay form
            driver.find_element(By.NAME, "payee.name").send_keys("Electric Company")
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 Power St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("New York")
            driver.find_element(By.NAME, "payee.address.state").send_keys("NY")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("10001")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5551234567")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("12345")
            driver.find_element(By.NAME, "verifyAccount").send_keys("12345")
            driver.find_element(By.NAME, "amount").send_keys("50")

            self.take_screenshot(driver, "TC_BILL_02_01_form_filled")

            send_button = driver.find_element(By.XPATH, "//input[@value='Send Payment']")
            send_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_BILL_02_02_result")

            if "complete" in driver.page_source.lower() or "successful" in driver.page_source.lower():
                print("[PASS] PASS: Bill payment completed successfully")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Payment confirmation not displayed")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_BILL_02_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_payee_name(self):
        print("\n=== TC_BILL_03: Empty Payee Name Validation ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            # Fill all except payee name
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 Test St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("Test City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("TS")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5551111111")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("11111")
            driver.find_element(By.NAME, "verifyAccount").send_keys("11111")
            driver.find_element(By.NAME, "amount").send_keys("25")

            self.take_screenshot(driver, "TC_BILL_03_01_no_payee_name")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_BILL_03_02_result")

            errors = driver.find_elements(By.CLASS_NAME, "error")
            if len(errors) > 0 or "required" in driver.page_source.lower():
                print("[PASS] PASS: Validation error shown for empty payee name")
                self.passed += 1
            else:
                print("[FAIL] FAIL: BUG - No validation for empty payee name")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_BILL_03_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_account_number_mismatch(self):
        print("\n=== TC_BILL_04: Account Number Mismatch ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            driver.find_element(By.NAME, "payee.name").send_keys("Test Payee")
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 Test St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("ST")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5552222222")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("12345")
            driver.find_element(By.NAME, "verifyAccount").send_keys("99999")  # Mismatch
            driver.find_element(By.NAME, "amount").send_keys("10")

            self.take_screenshot(driver, "TC_BILL_04_01_account_mismatch")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_BILL_04_02_result")

            if "match" in driver.page_source.lower() or "error" in driver.page_source.lower():
                print("[PASS] PASS: Account mismatch error displayed")
                self.passed += 1
            else:
                print("[FAIL] FAIL: BUG - No validation for account number mismatch")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_BILL_04_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_negative_amount(self):
        print("\n=== TC_BILL_05: Negative Payment Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            driver.find_element(By.NAME, "payee.name").send_keys("Negative Test")
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("ST")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5553333333")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("55555")
            driver.find_element(By.NAME, "verifyAccount").send_keys("55555")
            driver.find_element(By.NAME, "amount").send_keys("-100")

            self.take_screenshot(driver, "TC_BILL_05_01_negative_amount")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_BILL_05_02_result")

            if "error" in driver.page_source.lower() or "invalid" in driver.page_source.lower():
                print("[PASS] PASS: Negative amount rejected")
                self.passed += 1
            else:
                print("[FAIL] FAIL: BUG - System accepted negative payment amount")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_BILL_05_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_xss_in_payee_name(self):
        print("\n=== TC_BILL_06: XSS Prevention in Payee Name (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            xss_payload = "<script>alert('XSS')</script>"

            driver.find_element(By.NAME, "payee.name").send_keys(xss_payload)
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("ST")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5554444444")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys("66666")
            driver.find_element(By.NAME, "verifyAccount").send_keys("66666")
            driver.find_element(By.NAME, "amount").send_keys("1")

            self.take_screenshot(driver, "TC_BILL_06_01_xss_attempt")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_BILL_06_02_result")

            try:
                alert = driver.switch_to.alert
                print("[FAIL] FAIL: XSS vulnerability - alert triggered")
                alert.accept()
                self.failed += 1
            except:
                print("[PASS] PASS: XSS attack prevented")
                self.passed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_BILL_06_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_sql_injection_in_account(self):
        print("\n=== TC_BILL_07: SQL Injection in Account Field (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/billpay.htm")
            time.sleep(2)

            sql_payload = "'; DROP TABLE accounts; --"

            driver.find_element(By.NAME, "payee.name").send_keys("SQL Test")
            driver.find_element(By.NAME, "payee.address.street").send_keys("123 St")
            driver.find_element(By.NAME, "payee.address.city").send_keys("City")
            driver.find_element(By.NAME, "payee.address.state").send_keys("ST")
            driver.find_element(By.NAME, "payee.address.zipCode").send_keys("12345")
            driver.find_element(By.NAME, "payee.phoneNumber").send_keys("5555555555")
            driver.find_element(By.NAME, "payee.accountNumber").send_keys(sql_payload)
            driver.find_element(By.NAME, "verifyAccount").send_keys(sql_payload)
            driver.find_element(By.NAME, "amount").send_keys("1")

            self.take_screenshot(driver, "TC_BILL_07_01_sql_injection")

            driver.find_element(By.XPATH, "//input[@value='Send Payment']").click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_BILL_07_02_result")

            page_lower = driver.page_source.lower()
            if "sql" not in page_lower and "database" not in page_lower and "exception" not in page_lower:
                print("[PASS] PASS: SQL injection handled safely")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Potential SQL injection vulnerability")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_BILL_07_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK BILL PAY TEST SUITE")
        print("="*60)

        self.test_billpay_page_access()
        self.test_valid_bill_payment()
        self.test_empty_payee_name()
        self.test_account_number_mismatch()
        self.test_negative_amount()
        self.test_xss_in_payee_name()
        self.test_sql_injection_in_account()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("BILL PAY TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}


if __name__ == "__main__":
    test_suite = TestBillPay()
    test_suite.run_all_tests()
