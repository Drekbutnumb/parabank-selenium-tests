"""
Main Test Runner for Parabank - All Test Suites
Executes all 9 additional test modules
"""

from test_billpay import TestBillPay
from test_find_transactions import TestFindTransactions
from test_request_loan import TestRequestLoan
from test_update_contact import TestUpdateContactInfo
from test_forgot_login import TestForgotLoginInfo
from test_account_activity import TestAccountActivity
from test_logout import TestLogout
from test_navigation import TestNavigationMenu
from test_account_statement import TestAccountStatement

def run_all_suites():
    print("\n" + "="*70)
    print("PARABANK COMPLETE TEST AUTOMATION - 9 ADDITIONAL MODULES")
    print("="*70)

    all_results = []

    # 1. Bill Pay
    print("\n[1/9] Running Bill Pay Tests...")
    billpay = TestBillPay()
    all_results.append(("Bill Pay", billpay.run_all_tests()))

    # 2. Find Transactions
    print("\n[2/9] Running Find Transactions Tests...")
    find_trans = TestFindTransactions()
    all_results.append(("Find Transactions", find_trans.run_all_tests()))

    # 3. Request Loan
    print("\n[3/9] Running Request Loan Tests...")
    loan = TestRequestLoan()
    all_results.append(("Request Loan", loan.run_all_tests()))

    # 4. Update Contact Info
    print("\n[4/9] Running Update Contact Info Tests...")
    update = TestUpdateContactInfo()
    all_results.append(("Update Contact Info", update.run_all_tests()))

    # 5. Forgot Login
    print("\n[5/9] Running Forgot Login Tests...")
    forgot = TestForgotLoginInfo()
    all_results.append(("Forgot Login", forgot.run_all_tests()))

    # 6. Account Activity
    print("\n[6/9] Running Account Activity Tests...")
    activity = TestAccountActivity()
    all_results.append(("Account Activity", activity.run_all_tests()))

    # 7. Logout
    print("\n[7/9] Running Logout Tests...")
    logout = TestLogout()
    all_results.append(("Logout", logout.run_all_tests()))

    # 8. Navigation
    print("\n[8/9] Running Navigation Tests...")
    nav = TestNavigationMenu()
    all_results.append(("Navigation", nav.run_all_tests()))

    # 9. Account Statement
    print("\n[9/9] Running Account Statement Tests...")
    stmt = TestAccountStatement()
    all_results.append(("Account Statement", stmt.run_all_tests()))

    # Final Summary
    print("\n" + "="*70)
    print("FINAL SUMMARY - ALL TEST SUITES")
    print("="*70)

    total_tests = 0
    total_passed = 0
    total_failed = 0

    for name, result in all_results:
        total_tests += result["total"]
        total_passed += result["passed"]
        total_failed += result["failed"]
        status = "✓" if result["failed"] == 0 else "✗"
        print(f"{status} {name}: {result['passed']}/{result['total']} passed ({result['success_rate']:.1f}%)")

    overall_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print("\n" + "-"*70)
    print(f"TOTAL: {total_tests} tests | PASSED: {total_passed} | FAILED: {total_failed}")
    print(f"OVERALL SUCCESS RATE: {overall_rate:.2f}%")
    print("="*70)

    return {
        "total": total_tests,
        "passed": total_passed,
        "failed": total_failed,
        "success_rate": overall_rate,
        "details": all_results
    }


if __name__ == "__main__":
    run_all_suites()