pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                bat 'pip install selenium webdriver-manager'
            }
        }

        stage('Run All Tests & Generate Report') {
            steps {
                bat 'python generate_report.py'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'test_report.html', allowEmptyArchive: true
            archiveArtifacts artifacts: 'screenshots/**/*.png', allowEmptyArchive: true
            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'test_report.html',
                reportName: 'Selenium Test Report'
            ])
        }
    }
}