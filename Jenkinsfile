pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                bat 'C:\\Users\\yashr\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                bat 'C:\\Users\\yashr\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m pytest test_app.py -v'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying app...'
                echo 'App deployed successfully!'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed! Self-healing controller will handle this later.'
        }
    }
}
