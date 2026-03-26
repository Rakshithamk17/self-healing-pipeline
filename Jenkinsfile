pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                bat 'pytest test_app.py -v'
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
