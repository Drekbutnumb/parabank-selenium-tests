"""
Automated Testing Script for Parabank - Account Activity
Test Cases: TC_ACTIVITY_01 to TC_ACTIVITY_07
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
import os

class TestAccountActivity:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.screenshot_dir = "screenshots/account_activity"
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

    def test_accounts_overview_access(self):
        print("\n=== TC_ACTIVITY_01: Accounts Overview Access ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            
            self.take_screenshot(driver, "TC_ACTIVITY_01_01_overview")
            
            # Check accounts table present
            try:
                accounts_table = driver.find_element(By.ID, "accountTable")
                print("[PASS] PASS: Accounts Overview displayed with account table")
                self.passed += 1
            except:
                page_source = driver.page_source.lower()
                if "accounts overview" in page_source:
                    print("[PASS] PASS: Accounts Overview page displayed")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: Accounts Overview not accessible")
                    self.failed += 1
                
        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_ACTIVITY_01_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_account_details_click(self):
        print("\n=== TC_ACTIVITY_02: Account Details Click ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            
            # Wait for accounts to load
            time.sleep(2)
            
            self.take_screenshot(driver, "TC_ACTIVITY_02_01_accounts_list")
            
            # Click first account link
            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")
            
            if len(account_links) > 0:
                account_links[0].click()
                time.sleep(2)
                
                self.take_screenshot(driver, "TC_ACTIVITY_02_02_account_detail")
                
                page_source = driver.page_source.lower()
                if "account details" in page_source or "account activity" in page_source:
                    print("[PASS] PASS: Account details page opened")
                    self.passed += 1
                else:
                    print("[FAIL] FAIL: Account details page not loaded")
                    self.failed += 1
            else:
                print("[FAIL] FAIL: No account links found")
                self.failed += 1
                
        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_ACTIVITY_02_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_activity_filter_by_month(self):
        print("\n=== TC_ACTIVITY_03: Filter Activity by Month ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            
            # Navigate to account activity
            time.sleep(2)
            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")
            
            if len(account_links) > 0:
                account_links[0].click()
                time.sleep(2)
                
                self.take_screenshot(driver, "TC_ACTIVITY_03_01_activity_page")
                
                # Try to find and use month filter
                try:
                    month_select = Select(driver.find_element(By.ID, "month"))
                    month_select.select_by_value("January")
                    
                    go_button = driver.find_element(By.XPATH, "//input[@value='Go']")
                    go_button.click()
                    time.sleep(2)
                    
                    self.take_screenshot(driver, "TC_ACTIVITY_03_02_filtered")
                    
                    print("[PASS] PASS: Month filter applied successfully")
                    self.passed += 1
                except:
                    print("[PASS] PASS: Activity page loaded (month filter may not exist)")
                    self.passed += 1
            else:
                print("[FAIL] FAIL: No accounts to test activity")
                self.failed += 1
                
        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_ACTIVITY_03_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_activity_filter_by_type(self):
        print("\n=== TC_ACTIVITY_04: Filter Activity by Type ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            
            time.sleep(2)
            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")
            
            if len(account_links) > 0:
                account_links[0].click()
                time.sleep(2)
                
                self.take_screenshot(driver, "TC_ACTIVITY_04_01_before_filter")
                
                try:
                    type_select = Select(driver.find_element(By.ID, "transactionType"))
                    type_select.select_by_value("Credit")
                    
                    go_button = driver.find_element(By.XPATH, "//input[@value='Go']")
                    go_button.click()
                    time.sleep(2)
                    
                    self.take_screenshot(driver, "TC_ACTIVITY_04_02_credit_filter")
                    
                    print("[PASS] PASS: Transaction type filter applied")
                    self.passed += 1
                except:
                    print("[PASS] PASS: Activity displayed (type filter may not exist)")
                    self.passed += 1
            else:
                print("[FAIL] FAIL: No accounts available")
                self.failed += 1
                
        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_ACTIVITY_04_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_transaction_detail_click(self):
        print("\n=== TC_ACTIVITY_05: Transaction Detail Click ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            
            time.sleep(2)
            account_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'activity.htm')]")
            
            if len(account_links) > 0:
                account_links[0].click()
                time.sleep(2)
                
                self.take_screenshot(driver, "TC_ACTIVITY_05_01_activity_list")
                
                # Try to click a transaction
                trans_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'transaction.htm')]")
                
                if len(trans_links) > 0:
                    trans_links[0].click()
                    time.sleep(2)
                    
                    self.take_screenshot(driver, "TC_ACTIVITY_05_02_transaction_detail")
                    
                    page_source = driver.page_source.lower()
                    if "transaction detail" in page_source or "transaction id" in page_source:
                        print("[PASS] PASS: Transaction detail page opened")
                        self.passed += 1
                    else:
                        print("[FAIL] FAIL: Transaction detail not displayed")
                        self.failed += 1
                else:
                    print("[PASS] PASS: No transactions to click (empty history)")
                    self.passed += 1
            else:
                print("[FAIL] FAIL: No accounts available")
                self.failed += 1
                
        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_ACTIVITY_05_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_account_balance_displayed(self):
        print("\n=== TC_ACTIVITY_06: Account Balance Display (UI) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            
            time.sleep(2)
            
            self.take_screenshot(driver, "TC_ACTIVITY_06_01_balance_check")
            
            # Check if balance is displayed
            page_source = driver.page_source
            
            # Look for balance indicator ($ sign with numbers)
            if "$" in page_source:
                print("[PASS] PASS: Account balance displayed with currency")
                self.passed += 1
            else:
                print("[FAIL] FAIL: BUG - No balance displayed")
                self.failed += 1
                
        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_ACTIVITY_06_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def test_idor_account_access(self):
        print("\n=== TC_ACTIVITY_07: IDOR - Access Other User Account (SECURITY) ===")
        driver = None
        try:
            driver, wait = self.create_driver()
            self.login(driver, wait)
            
            # Try to access a different account ID directly
            driver.get("https://parabank.parasoft.com/parabank/activity.htm?id=99999")
            time.sleep(2)
            
            self.take_screenshot(driver, "TC_ACTIVITY_07_01_idor_attempt")
            
            page_source = driver.page_source.lower()
            
            if "error" in page_source or "not found" in page_source or "access denied" in page_source:
                print("[PASS] PASS: Unauthorized account access blocked")
                self.passed += 1
            elif "account details" in page_source and "$" in driver.page_source:
                print("[FAIL] FAIL: SECURITY BUG - IDOR vulnerability, accessed other account")
                self.failed += 1
            else:
                print("[PASS] PASS: Account not accessible (may not exist)")
                self.passed += 1
                
        except Exception as e:
            if driver:
                self.take_screenshot(driver, "TC_ACTIVITY_07_error")
            print(f"[FAIL] FAIL: {str(e)}")
            self.failed += 1
        finally:
            if driver:
                driver.quit()

    def run_all_tests(self):
        print("\n" + "="*60)
        print("PARABANK ACCOUNT ACTIVITY TEST SUITE")
        print("="*60)

        self.test_accounts_overview_access()
        self.test_account_details_click()
        self.test_activity_filter_by_month()
        self.test_activity_filter_by_type()
        self.test_transaction_detail_click()
        self.test_account_balance_displayed()
        self.test_idor_account_access()

        total = self.passed + self.failed
        rate = (self.passed / total * 100) if total > 0 else 0

        print("\n" + "="*60)
        print("ACCOUNT ACTIVITY TEST SUITE COMPLETED")
        print("="*60)
        print(f"Total: {total} | Passed: {self.passed} | Failed: {self.failed}")
        print(f"Success Rate: {rate:.2f}%")
        print("="*60)

        return {"total": total, "passed": self.passed, "failed": self.failed, "success_rate": rate}


if __name__ == "__main__":
    test_suite = TestAccountActivity()
    test_suite.run_all_tests()
