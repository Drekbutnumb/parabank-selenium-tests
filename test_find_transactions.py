"""
Automated Testing Script for Parabank - Find Transactions
Test Cases: TC_FIND_01 to TC_FIND_07
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

class TestFindTransactions:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.screenshot_dir = "screenshots/find_transactions"
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

    def test_find_transactions_page_access(self):
        print("\n=== TC_FIND_01: Find Transactions Page Access ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            find_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Find Transactions")))
            find_link.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_FIND_01_01_page_loaded")

            # Check page elements
            page_source = driver.page_source.lower()
            if "find transactions" in page_source and "select an account" in page_source:
                print("[PASS] PASS: Find Transactions page loaded with required elements")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Page elements missing")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_FIND_01_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_search_by_transaction_id(self):
        print("\n=== TC_FIND_02: Search by Transaction ID ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(3)

            # First select an account from dropdown
            account_select = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
            Select(account_select).select_by_index(0)
            time.sleep(1)

            # Enter transaction ID
            trans_id_field = driver.find_element(By.ID, "transactionId")
            trans_id_field.send_keys("12345")

            self.take_screenshot(driver, "TC_FIND_02_01_id_entered")

            # Click find by ID button
            find_button = driver.find_element(By.XPATH, "//button[@id='findById']")
            find_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_FIND_02_02_result")

            # Check for results - internal error is a BUG!
            page_source = driver.page_source.lower()
            if "internal error" in page_source or "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error when searching by Transaction ID")
                self.failed += 1
            elif "transaction results" in page_source or "no transactions found" in page_source:
                print("[PASS] PASS: Search by ID executed successfully with proper response")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Unexpected response from search")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_FIND_02_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_search_by_date(self):
        print("\n=== TC_FIND_03: Search by Date ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(3)

            # First select an account from dropdown
            account_select = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
            Select(account_select).select_by_index(0)
            time.sleep(1)

            date_field = driver.find_element(By.ID, "transactionDate")
            date_field.send_keys("01-01-2024")

            self.take_screenshot(driver, "TC_FIND_03_01_date_entered")

            find_button = driver.find_element(By.XPATH, "//button[@id='findByDate']")
            find_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_FIND_03_02_result")

            # Check for results - internal error is a BUG!
            page_source = driver.page_source.lower()
            if "internal error" in page_source or "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error when searching by Date")
                self.failed += 1
            elif "transaction results" in page_source or "no transactions found" in page_source:
                print("[PASS] PASS: Search by date executed successfully with proper response")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Unexpected response from date search")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_FIND_03_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_search_by_amount(self):
        print("\n=== TC_FIND_04: Search by Amount ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(3)

            # First select an account from dropdown
            account_select = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
            Select(account_select).select_by_index(0)
            time.sleep(1)

            amount_field = driver.find_element(By.ID, "amount")
            amount_field.send_keys("100")

            self.take_screenshot(driver, "TC_FIND_04_01_amount_entered")

            find_button = driver.find_element(By.XPATH, "//button[@id='findByAmount']")
            find_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_FIND_04_02_result")

            # Check for results - internal error is a BUG!
            page_source = driver.page_source.lower()
            if "internal error" in page_source or "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error when searching by Amount")
                self.failed += 1
            elif "transaction results" in page_source or "no transactions found" in page_source:
                print("[PASS] PASS: Search by amount executed successfully with proper response")
                self.passed += 1
            else:
                print("[FAIL] FAIL: Unexpected response from amount search")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_FIND_04_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_empty_transaction_id(self):
        print("\n=== TC_FIND_05: Empty Transaction ID Validation ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(3)

            # First select an account from dropdown
            account_select = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
            Select(account_select).select_by_index(0)
            time.sleep(1)

            self.take_screenshot(driver, "TC_FIND_05_01_empty_field")

            # Click find without entering ID
            find_button = driver.find_element(By.XPATH, "//button[@id='findById']")
            find_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_FIND_05_02_result")

            page_source = driver.page_source.lower()
            # Internal error is a BUG - should show proper validation message instead
            if "internal error" in page_source or "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error instead of validation message for empty ID")
                self.failed += 1
            elif "required" in page_source or "please enter" in page_source or "invalid" in page_source:
                print("[PASS] PASS: Proper validation error shown for empty ID")
                self.passed += 1
            else:
                print("[FAIL] FAIL: BUG - No validation for empty transaction ID")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_FIND_05_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_invalid_date_format(self):
        print("\n=== TC_FIND_06: Invalid Date Format ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(3)

            # First select an account from dropdown
            account_select = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
            Select(account_select).select_by_index(0)
            time.sleep(1)

            date_field = driver.find_element(By.ID, "transactionDate")
            date_field.send_keys("invalid-date-format")

            self.take_screenshot(driver, "TC_FIND_06_01_invalid_date")

            find_button = driver.find_element(By.XPATH, "//button[@id='findByDate']")
            find_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_FIND_06_02_result")

            page_source = driver.page_source.lower()
            # Internal error is a BUG - should show proper validation message instead
            if "internal error" in page_source or "an internal error has occurred" in page_source:
                print("[FAIL] FAIL: BUG FOUND - Internal server error instead of validation for invalid date format")
                self.failed += 1
            elif "invalid date" in page_source or "please enter a valid" in page_source or "format" in page_source:
                print("[PASS] PASS: Invalid date format properly rejected with validation message")
                self.passed += 1
            else:
                print("[FAIL] FAIL: BUG - System accepted invalid date format without proper validation")
                self.failed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_FIND_06_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_sql_injection_in_search(self):
        print("\n=== TC_FIND_07: SQL Injection in Transaction ID (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)

            driver.get("https://parabank.parasoft.com/parabank/findtrans.htm")
            time.sleep(3)

            # First select an account from dropdown
            account_select = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
            Select(account_select).select_by_index(0)
            time.sleep(1)

            sql_payload = "1 OR 1=1; --"

            trans_id_field = driver.find_element(By.ID, "transactionId")
            trans_id_field.send_keys(sql_payload)

            self.take_screenshot(driver, "TC_FIND_07_01_sql_injection")

            find_button = driver.find_element(By.XPATH, "//button[@id='findById']")
            find_button.click()
            time.sleep(2)

            self.take_screenshot(driver, "TC_FIND_07_02_result")

            page_lower = driver.page_source.lower()
            # Check for various security issues
            if "sql" in page_lower or "database" in page_lower or "exception" in page_lower or "syntax" in page_lower:
                print("[FAIL] FAIL: SECURITY BUG - SQL injection vulnerability detected (database error exposed)")
                self.failed += 1
            elif "internal error" in page_lower or "an internal error has occurred" in page_lower:
                print("[FAIL] FAIL: BUG FOUND - Internal server error when handling SQL injection input")
                self.failed += 1
            elif "invalid" in page_lower or "not found" in page_lower or "no transactions" in page_lower:
                print("[PASS] PASS: SQL injection handled safely with proper response")
                self.passed += 1
            else:
                print("[PASS] PASS: SQL injection input rejected without exposing system details")
                self.passed += 1

        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_FIND_07_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK FIND TRANSACTIONS TEST SUITE")
        print("="*60)

        self.test_find_transactions_page_access()
        self.test_search_by_transaction_id()
        self.test_search_by_date()
        self.test_search_by_amount()
        self.test_empty_transaction_id()
        self.test_invalid_date_format()
        self.test_sql_injection_in_search()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("FIND TRANSACTIONS TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}


if __name__ == "__main__":
    test_suite = TestFindTransactions()
    test_suite.run_all_tests()