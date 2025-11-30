"""
HTML Test Report Generator for Parabank Selenium Tests
Generates a professional HTML report after all tests complete
"""

import os
import sys
from datetime import datetime
import glob

class TestReportGenerator:
    def __init__(self):
        self.test_results = []
        self.total_passed = 0
        self.total_failed = 0
        self.start_time = datetime.now()
        
    def run_all_tests(self):
        """Run all test suites and collect results"""
        
        # Import and run each test suite
        test_suites = [
            ("Registration", "test_selenium1", "TestRegistration"),
            ("Login", "test_selenium2", "TestLogin"),
            ("Open Account", "test_selenium3", "TestOpenAccount"),
            ("Transfer Funds", "test_selenium4", "TestTransferFunds"),
            ("Accounts Overview", "test_selenium5", "TestAccountsOverview"),
            ("Admin Page", "test_selenium6", "TestAdminPage"),
            ("Customer Care", "test_selenium7", "TestCustomerCare"),
        ]
        
        for suite_name, module_name, class_name in test_suites:
            try:
                # Dynamic import
                module = __import__(module_name)
                test_class = getattr(module, class_name)
                
                print(f"\n{'='*60}")
                print(f"Running {suite_name} Tests...")
                print('='*60)
                
                # Run tests
                test_instance = test_class()
                result = test_instance.run_all_tests()
                
                self.test_results.append({
                    "name": suite_name,
                    "module": module_name,
                    "passed": result["passed"],
                    "failed": result["failed"],
                    "total": result["total"],
                    "success_rate": result["success_rate"]
                })
                
                self.total_passed += result["passed"]
                self.total_failed += result["failed"]
                
            except Exception as e:
                print(f"[ERROR] Failed to run {suite_name}: {str(e)}")
                self.test_results.append({
                    "name": suite_name,
                    "module": module_name,
                    "passed": 0,
                    "failed": 1,
                    "total": 1,
                    "success_rate": 0,
                    "error": str(e)
                })
                self.total_failed += 1
    
    def count_screenshots(self):
        """Count total screenshots captured"""
        screenshots = glob.glob("screenshots/**/*.png", recursive=True)
        return len(screenshots)
    
    def generate_html_report(self):
        """Generate the HTML report"""
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        total_tests = self.total_passed + self.total_failed
        success_rate = (self.total_passed / total_tests * 100) if total_tests > 0 else 0
        screenshot_count = self.count_screenshots()
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parabank Test Report - {end_time.strftime("%Y-%m-%d %H:%M")}</title>
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #334155;
            --accent-green: #22c55e;
            --accent-red: #ef4444;
            --accent-blue: #3b82f6;
            --accent-yellow: #eab308;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border: #475569;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        /* Header */
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: var(--bg-secondary);
            border-radius: 16px;
            border: 1px solid var(--border);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            color: var(--accent-blue);
        }}
        
        .header .subtitle {{
            color: var(--text-secondary);
            font-size: 1.1rem;
        }}
        
        .header .timestamp {{
            margin-top: 15px;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }}
        
        /* Summary Cards */
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .summary-card {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            border: 1px solid var(--border);
            transition: transform 0.2s;
        }}
        
        .summary-card:hover {{
            transform: translateY(-5px);
        }}
        
        .summary-card .value {{
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        
        .summary-card .label {{
            color: var(--text-secondary);
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }}
        
        .summary-card.total .value {{ color: var(--accent-blue); }}
        .summary-card.passed .value {{ color: var(--accent-green); }}
        .summary-card.failed .value {{ color: var(--accent-red); }}
        .summary-card.rate .value {{ color: var(--accent-yellow); }}
        
        /* Progress Bar */
        .progress-section {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 40px;
            border: 1px solid var(--border);
        }}
        
        .progress-section h3 {{
            margin-bottom: 15px;
            color: var(--text-secondary);
        }}
        
        .progress-bar {{
            height: 30px;
            background: var(--bg-card);
            border-radius: 15px;
            overflow: hidden;
            display: flex;
        }}
        
        .progress-passed {{
            background: linear-gradient(90deg, #22c55e, #16a34a);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9rem;
        }}
        
        .progress-failed {{
            background: linear-gradient(90deg, #ef4444, #dc2626);
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9rem;
        }}
        
        /* Test Suites Table */
        .suites-section {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 40px;
            border: 1px solid var(--border);
        }}
        
        .suites-section h2 {{
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .suites-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .suites-table th,
        .suites-table td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        
        .suites-table th {{
            background: var(--bg-card);
            color: var(--text-secondary);
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }}
        
        .suites-table tr:hover {{
            background: rgba(59, 130, 246, 0.1);
        }}
        
        .suite-name {{
            font-weight: 600;
            color: var(--accent-blue);
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        
        .badge-passed {{
            background: rgba(34, 197, 94, 0.2);
            color: var(--accent-green);
        }}
        
        .badge-failed {{
            background: rgba(239, 68, 68, 0.2);
            color: var(--accent-red);
        }}
        
        .rate-bar {{
            width: 100px;
            height: 8px;
            background: var(--bg-card);
            border-radius: 4px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
            margin-right: 10px;
        }}
        
        .rate-bar-fill {{
            height: 100%;
            border-radius: 4px;
        }}
        
        .rate-100 {{ background: var(--accent-green); }}
        .rate-75 {{ background: var(--accent-yellow); }}
        .rate-50 {{ background: #f97316; }}
        .rate-low {{ background: var(--accent-red); }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 20px;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}
        
        .footer a {{
            color: var(--accent-blue);
            text-decoration: none;
        }}
        
        /* Status Icon */
        .status-icon {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        
        .status-pass {{ background: var(--accent-green); box-shadow: 0 0 10px var(--accent-green); }}
        .status-fail {{ background: var(--accent-red); box-shadow: 0 0 10px var(--accent-red); }}
        
        /* Info Cards */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .info-card {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border);
        }}
        
        .info-card h4 {{
            color: var(--text-secondary);
            margin-bottom: 10px;
            font-size: 0.9rem;
        }}
        
        .info-card p {{
            font-size: 1.1rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>PARABANK TEST REPORT</h1>
            <p class="subtitle">Selenium Automation Test Suite Results</p>
            <p class="timestamp">Generated: {end_time.strftime("%B %d, %Y at %H:%M:%S")}</p>
        </div>
        
        <!-- Summary Cards -->
        <div class="summary-grid">
            <div class="summary-card total">
                <div class="value">{total_tests}</div>
                <div class="label">Total Tests</div>
            </div>
            <div class="summary-card passed">
                <div class="value">{self.total_passed}</div>
                <div class="label">Passed</div>
            </div>
            <div class="summary-card failed">
                <div class="value">{self.total_failed}</div>
                <div class="label">Failed</div>
            </div>
            <div class="summary-card rate">
                <div class="value">{success_rate:.1f}%</div>
                <div class="label">Success Rate</div>
            </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="progress-section">
            <h3>Overall Progress</h3>
            <div class="progress-bar">
                <div class="progress-passed" style="width: {success_rate}%">
                    {self.total_passed} Passed
                </div>
                <div class="progress-failed" style="width: {100 - success_rate}%">
                    {self.total_failed if self.total_failed > 0 else ''} {'Failed' if self.total_failed > 0 else ''}
                </div>
            </div>
        </div>
        
        <!-- Info Cards -->
        <div class="info-grid">
            <div class="info-card">
                <h4>EXECUTION TIME</h4>
                <p>{duration:.1f} seconds</p>
            </div>
            <div class="info-card">
                <h4>TEST SUITES</h4>
                <p>{len(self.test_results)} suites</p>
            </div>
            <div class="info-card">
                <h4>SCREENSHOTS CAPTURED</h4>
                <p>{screenshot_count} images</p>
            </div>
            <div class="info-card">
                <h4>BUILD STATUS</h4>
                <p><span class="status-icon {'status-pass' if self.total_failed == 0 else 'status-fail'}"></span>{'SUCCESS' if self.total_failed == 0 else 'UNSTABLE'}</p>
            </div>
        </div>
        
        <!-- Test Suites Table -->
        <div class="suites-section">
            <h2>Test Suite Results</h2>
            <table class="suites-table">
                <thead>
                    <tr>
                        <th>Suite Name</th>
                        <th>Module</th>
                        <th>Total</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Success Rate</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
'''
        
        # Add rows for each test suite
        for suite in self.test_results:
            rate = suite["success_rate"]
            rate_class = "rate-100" if rate == 100 else "rate-75" if rate >= 75 else "rate-50" if rate >= 50 else "rate-low"
            status_class = "status-pass" if suite["failed"] == 0 else "status-fail"
            status_badge = "badge-passed" if suite["failed"] == 0 else "badge-failed"
            status_text = "PASS" if suite["failed"] == 0 else "FAIL"
            
            html += f'''
                    <tr>
                        <td class="suite-name">{suite["name"]}</td>
                        <td>{suite["module"]}.py</td>
                        <td>{suite["total"]}</td>
                        <td style="color: var(--accent-green)">{suite["passed"]}</td>
                        <td style="color: var(--accent-red)">{suite["failed"]}</td>
                        <td>
                            <div class="rate-bar"><div class="rate-bar-fill {rate_class}" style="width: {rate}%"></div></div>
                            {rate:.1f}%
                        </td>
                        <td><span class="badge {status_badge}">{status_text}</span></td>
                    </tr>
'''
        
        html += f'''
                </tbody>
            </table>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <p>Parabank Selenium Test Automation | Generated by Jenkins CI/CD Pipeline</p>
            <p>Test Framework: Python + Selenium WebDriver</p>
        </div>
    </div>
</body>
</html>
'''
        
        # Write HTML file
        report_path = "test_report.html"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"\n{'='*60}")
        print("HTML REPORT GENERATED")
        print('='*60)
        print(f"Report saved to: {report_path}")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.total_passed}")
        print(f"Failed: {self.total_failed}")
        print(f"Success Rate: {success_rate:.1f}%")
        print('='*60)
        
        return report_path


if __name__ == "__main__":
    generator = TestReportGenerator()
    generator.run_all_tests()
    generator.generate_html_report()
