pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                bat 'pip install selenium webdriver-manager'
            }
        }

        stage('Run Registration Tests') {
            steps {
                bat 'python test_selenium1.py'
            }
        }

        stage('Run Login Tests') {
            steps {
                bat 'python test_selenium2.py'
            }
        }

        stage('Run Open Account Tests') {
            steps {
                bat 'python test_selenium3.py'
            }
        }

        stage('Run Transfer Tests') {
            steps {
                bat 'python test_selenium4.py'
            }
        }

        stage('Run Accounts Overview Tests') {
            steps {
                bat 'python test_selenium5.py'
            }
        }

        stage('Run Admin Page Tests') {
            steps {
                bat 'python test_selenium6.py'
            }
        }

        stage('Run Customer Care Tests') {
            steps {
                bat 'python test_selenium7.py'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'screenshots/**/*.png', allowEmptyArchive: true
        }
    }
}