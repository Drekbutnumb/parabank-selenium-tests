"""
ParaBank Test Runner - Run All 16 Selenium Test Suites
"""

from test_selenium1 import TestRegistration
from test_selenium2 import TestLogin
from test_selenium3 import TestOpenAccount
from test_selenium4 import TestTransferFunds
from test_selenium5 import TestAccountsOverview
from test_selenium6 import TestAdminPage
from test_selenium7 import TestCustomerCare
from test_billpay import TestBillPay
from test_find_transactions import TestFindTransactions
from test_request_loan import TestRequestLoan
from test_update_contact import TestUpdateContactInfo
from test_forgot_login import TestForgotLoginInfo
from test_account_activity import TestAccountActivity
from test_logout import TestLogout
from test_navigation import TestNavigationMenu
from test_account_statement import TestAccountStatement

def run_all():
    print("\n" + "="*70)
    print("PARABANK COMPLETE TEST SUITE - 16 MODULES")
    print("="*70)

    all_results = []

    suites = [
        ("1. Registration", TestRegistration),
        ("2. Login", TestLogin),
        ("3. Open Account", TestOpenAccount),
        ("4. Transfer Funds", TestTransferFunds),
        ("5. Accounts Overview", TestAccountsOverview),
        ("6. Admin Page", TestAdminPage),
        ("7. Customer Care", TestCustomerCare),
        ("8. Bill Pay", TestBillPay),
        ("9. Find Transactions", TestFindTransactions),
        ("10. Request Loan", TestRequestLoan),
        ("11. Update Contact", TestUpdateContactInfo),
        ("12. Forgot Login", TestForgotLoginInfo),
        ("13. Account Activity", TestAccountActivity),
        ("14. Logout", TestLogout),
        ("15. Navigation", TestNavigationMenu),
        ("16. Account Statement", TestAccountStatement),
    ]

    for name, TestClass in suites:
        print(f"\n[{name}] Running...")
        try:
            test = TestClass()
            result = test.run_all_tests()
            all_results.append((name, result))
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            all_results.append((name, {"passed": 0, "failed": 0, "total": 0, "success_rate": 0}))

    # Final Summary
    print("\n" + "="*70)
    print("FINAL SUMMARY - ALL TEST SUITES")
    print("="*70)

    total_tests = 0
    total_passed = 0
    total_failed = 0

    for name, result in all_results:
        total_tests += result.get("total", 0)
        total_passed += result.get("passed", 0)
        total_failed += result.get("failed", 0)
        status = "PASS" if result.get("failed", 0) == 0 else "BUGS"
        print(f"{status} {name}: {result.get('passed', 0)}/{result.get('total', 0)} ({result.get('success_rate', 0):.1f}%)")

    overall_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print("\n" + "-"*70)
    print(f"TOTAL: {total_tests} tests | PASSED: {total_passed} | FAILED: {total_failed}")
    print(f"OVERALL SUCCESS RATE: {overall_rate:.2f}%")
    print("="*70)


if __name__ == "__main__":
    run_all()