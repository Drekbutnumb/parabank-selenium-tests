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
                module = __import__(module_name)
                test_class = getattr(module, class_name)

                print(f"\n{'='*60}")
                print(f"Running {suite_name} Tests...")
                print('='*60)

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

        # Generate table rows
        table_rows = ""
        for suite in self.test_results:
            rate = suite["success_rate"]
            rate_class = "rate-100" if rate == 100 else "rate-75" if rate >= 75 else "rate-50" if rate >= 50 else "rate-low"
            status_badge = "badge-passed" if suite["failed"] == 0 else "badge-failed"
            status_text = "PASS" if suite["failed"] == 0 else "FAIL"

            table_rows += f'''
                    <tr>
                        <td class="suite-name">{suite["name"]}</td>
                        <td class="module-name">{suite["module"]}.py</td>
                        <td class="num-total">{suite["total"]}</td>
                        <td class="num-passed">{suite["passed"]}</td>
                        <td class="num-failed">{suite["failed"]}</td>
                        <td>
                            <div class="rate-bar"><div class="rate-bar-fill {rate_class}" style="width: {rate}%"></div></div>
                            <span class="rate-text">{rate:.0f}%</span>
                        </td>
                        <td><span class="badge {status_badge}">{status_text}</span></td>
                    </tr>'''

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parabank Test Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: #1a2332;
            --accent-cyan: #00f0ff;
            --accent-green: #00ff88;
            --accent-red: #ff3366;
            --accent-yellow: #ffcc00;
            --accent-purple: #a855f7;
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border-color: #2d3748;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Rajdhani', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }}
        .bg-grid {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
            background-size: 60px 60px;
            pointer-events: none;
            animation: gridMove 20s linear infinite;
        }}
        @keyframes gridMove {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(60px, 60px); }}
        }}
        .orb {{
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.12;
            pointer-events: none;
        }}
        .orb-1 {{ width: 500px; height: 500px; background: var(--accent-cyan); top: -150px; right: -150px; }}
        .orb-2 {{ width: 400px; height: 400px; background: var(--accent-purple); bottom: -100px; left: -100px; }}
        .container {{
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 50px;
            padding: 50px 40px;
            background: linear-gradient(135deg, rgba(26, 35, 50, 0.95) 0%, rgba(17, 24, 39, 0.95) 100%);
            border-radius: 24px;
            border: 1px solid var(--accent-cyan);
            box-shadow: 0 0 30px rgba(0, 240, 255, 0.2);
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-purple), var(--accent-cyan), transparent);
        }}
        .header h1 {{
            font-family: 'Orbitron', monospace;
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 15px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: 4px;
        }}
        .header .subtitle {{
            color: var(--text-secondary);
            font-size: 1.3rem;
            font-weight: 500;
            letter-spacing: 3px;
            text-transform: uppercase;
        }}
        .header .timestamp {{
            margin-top: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: var(--accent-cyan);
            padding: 8px 20px;
            background: rgba(0, 240, 255, 0.1);
            border-radius: 30px;
            display: inline-block;
            border: 1px solid rgba(0, 240, 255, 0.3);
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            margin-bottom: 50px;
        }}
        @media (max-width: 900px) {{ .summary-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media (max-width: 500px) {{ .summary-grid {{ grid-template-columns: 1fr; }} }}
        .summary-card {{
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
            border-radius: 20px;
            padding: 35px 25px;
            text-align: center;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }}
        .summary-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }}
        .summary-card .value {{
            font-family: 'Orbitron', monospace;
            font-size: 3.2rem;
            font-weight: 800;
            margin-bottom: 10px;
        }}
        .summary-card .label {{
            color: var(--text-secondary);
            text-transform: uppercase;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 2px;
        }}
        .summary-card.total {{ border-color: var(--accent-cyan); }}
        .summary-card.total .value {{ color: var(--accent-cyan); text-shadow: 0 0 20px rgba(0, 240, 255, 0.5); }}
        .summary-card.passed {{ border-color: var(--accent-green); }}
        .summary-card.passed .value {{ color: var(--accent-green); text-shadow: 0 0 20px rgba(0, 255, 136, 0.5); }}
        .summary-card.failed {{ border-color: var(--accent-red); }}
        .summary-card.failed .value {{ color: var(--accent-red); text-shadow: 0 0 20px rgba(255, 51, 102, 0.5); }}
        .summary-card.rate {{ border-color: var(--accent-yellow); }}
        .summary-card.rate .value {{ color: var(--accent-yellow); text-shadow: 0 0 20px rgba(255, 204, 0, 0.5); }}
        .progress-section {{
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
            border-radius: 24px;
            padding: 40px;
            margin-bottom: 50px;
            border: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 50px;
        }}
        @media (max-width: 800px) {{ .progress-section {{ flex-direction: column; }} }}
        .circular-progress {{
            position: relative;
            width: 180px;
            height: 180px;
            flex-shrink: 0;
        }}
        .circular-progress svg {{
            transform: rotate(-90deg);
            width: 180px;
            height: 180px;
        }}
        .circular-progress .bg {{
            fill: none;
            stroke: var(--bg-primary);
            stroke-width: 14;
        }}
        .circular-progress .progress-ring {{
            fill: none;
            stroke: url(#grad);
            stroke-width: 14;
            stroke-linecap: round;
            stroke-dasharray: 502;
            stroke-dashoffset: {502 - (502 * success_rate / 100)};
            filter: drop-shadow(0 0 8px rgba(0, 255, 136, 0.6));
        }}
        .circular-progress .percentage {{
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }}
        .circular-progress .percentage .value {{
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--accent-green);
            text-shadow: 0 0 15px rgba(0, 255, 136, 0.5);
        }}
        .circular-progress .percentage .label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .progress-details {{ flex: 1; }}
        .progress-details h3 {{
            font-family: 'Orbitron', monospace;
            font-size: 1.4rem;
            margin-bottom: 25px;
            color: var(--text-primary);
        }}
        .progress-bar-container {{ margin-bottom: 18px; }}
        .progress-bar-label {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.95rem;
        }}
        .progress-bar {{
            height: 12px;
            background: var(--bg-primary);
            border-radius: 10px;
            overflow: hidden;
        }}
        .progress-bar-fill {{
            height: 100%;
            border-radius: 10px;
        }}
        .progress-bar-fill.passed {{
            background: linear-gradient(90deg, #00ff88, #00cc6a);
            box-shadow: 0 0 12px rgba(0, 255, 136, 0.5);
        }}
        .progress-bar-fill.failed {{
            background: linear-gradient(90deg, #ff3366, #cc2952);
            box-shadow: 0 0 12px rgba(255, 51, 102, 0.5);
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 50px;
        }}
        @media (max-width: 900px) {{ .info-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        .info-card {{
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
            border-radius: 16px;
            padding: 22px;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }}
        .info-card:hover {{ border-color: var(--accent-cyan); transform: translateY(-3px); }}
        .info-card h4 {{
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-muted);
            margin-bottom: 10px;
            font-size: 0.75rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        .info-card p {{
            font-size: 1.3rem;
            font-weight: 600;
        }}
        .status-icon {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
        @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}
        .status-pass {{ background: var(--accent-green); box-shadow: 0 0 12px var(--accent-green); }}
        .status-fail {{ background: var(--accent-red); box-shadow: 0 0 12px var(--accent-red); }}
        .suites-section {{
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
            border-radius: 24px;
            padding: 40px;
            margin-bottom: 50px;
            border: 1px solid var(--border-color);
        }}
        .suites-section h2 {{
            font-family: 'Orbitron', monospace;
            font-size: 1.6rem;
            margin-bottom: 30px;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .suites-section h2::before {{
            content: '';
            display: inline-block;
            width: 6px;
            height: 28px;
            background: linear-gradient(180deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 3px;
        }}
        .suites-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 8px;
        }}
        .suites-table th {{
            font-family: 'JetBrains Mono', monospace;
            background: var(--bg-primary);
            color: var(--text-muted);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 1px;
            padding: 14px 18px;
            text-align: left;
        }}
        .suites-table th:first-child {{ border-radius: 8px 0 0 8px; }}
        .suites-table th:last-child {{ border-radius: 0 8px 8px 0; }}
        .suites-table td {{
            padding: 18px;
            background: var(--bg-primary);
            transition: all 0.2s ease;
        }}
        .suites-table tr:hover td {{ background: rgba(0, 240, 255, 0.05); }}
        .suites-table td:first-child {{ border-radius: 8px 0 0 8px; }}
        .suites-table td:last-child {{ border-radius: 0 8px 8px 0; }}
        .suite-name {{
            font-weight: 700;
            font-size: 1.1rem;
            color: var(--accent-cyan);
        }}
        .module-name {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        .badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        .badge-passed {{
            background: rgba(0, 255, 136, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(0, 255, 136, 0.3);
        }}
        .badge-failed {{
            background: rgba(255, 51, 102, 0.15);
            color: var(--accent-red);
            border: 1px solid rgba(255, 51, 102, 0.3);
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
        .rate-100 {{ background: linear-gradient(90deg, #00ff88, #00cc6a); }}
        .rate-75 {{ background: linear-gradient(90deg, #ffcc00, #e6b800); }}
        .rate-50 {{ background: linear-gradient(90deg, #ff6b35, #e65a2b); }}
        .rate-low {{ background: linear-gradient(90deg, #ff3366, #cc2952); }}
        .rate-text {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            font-weight: 600;
        }}
        .num-passed {{ color: var(--accent-green); font-weight: 700; font-family: 'JetBrains Mono', monospace; }}
        .num-failed {{ color: var(--accent-red); font-weight: 700; font-family: 'JetBrains Mono', monospace; }}
        .num-total {{ font-weight: 600; font-family: 'JetBrains Mono', monospace; }}
        .footer {{
            text-align: center;
            padding: 30px 20px;
            color: var(--text-muted);
            font-size: 0.9rem;
        }}
        .footer .brand {{
            font-family: 'Orbitron', monospace;
            color: var(--accent-cyan);
        }}
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    
    <div class="container">
        <div class="header">
            <h1>PARABANK TEST REPORT</h1>
            <p class="subtitle">Selenium Automation Test Suite</p>
            <p class="timestamp">{end_time.strftime("%B %d, %Y at %H:%M:%S")}</p>
        </div>
        
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
                <div class="value">{success_rate:.0f}%</div>
                <div class="label">Success Rate</div>
            </div>
        </div>
        
        <div class="progress-section">
            <div class="circular-progress">
                <svg viewBox="0 0 180 180">
                    <defs>
                        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" style="stop-color:#00ff88"/>
                            <stop offset="100%" style="stop-color:#00f0ff"/>
                        </linearGradient>
                    </defs>
                    <circle class="bg" cx="90" cy="90" r="80"/>
                    <circle class="progress-ring" cx="90" cy="90" r="80"/>
                </svg>
                <div class="percentage">
                    <div class="value">{success_rate:.0f}%</div>
                    <div class="label">Success</div>
                </div>
            </div>
            <div class="progress-details">
                <h3>Execution Summary</h3>
                <div class="progress-bar-container">
                    <div class="progress-bar-label">
                        <span style="color: var(--accent-green)">Passed</span>
                        <span class="num-passed">{self.total_passed} tests</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-bar-fill passed" style="width: {success_rate}%"></div>
                    </div>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar-label">
                        <span style="color: var(--accent-red)">Failed</span>
                        <span class="num-failed">{self.total_failed} tests</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-bar-fill failed" style="width: {100 - success_rate}%"></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="info-grid">
            <div class="info-card">
                <h4>Execution Time</h4>
                <p>{duration:.1f} seconds</p>
            </div>
            <div class="info-card">
                <h4>Test Suites</h4>
                <p>{len(self.test_results)} suites</p>
            </div>
            <div class="info-card">
                <h4>Screenshots</h4>
                <p>{screenshot_count} captured</p>
            </div>
            <div class="info-card">
                <h4>Build Status</h4>
                <p><span class="status-icon {"status-pass" if self.total_failed == 0 else "status-fail"}"></span>{"SUCCESS" if self.total_failed == 0 else "UNSTABLE"}</p>
            </div>
        </div>
        
        <div class="suites-section">
            <h2>Test Suite Results</h2>
            <table class="suites-table">
                <thead>
                    <tr>
                        <th>Suite</th>
                        <th>Module</th>
                        <th>Total</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Rate</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>{table_rows}
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p><span class="brand">PARABANK</span> Selenium Test Automation</p>
            <p>Generated by Jenkins CI/CD Pipeline</p>
        </div>
    </div>
</body>
</html>'''

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