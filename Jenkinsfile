pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Setup Env') {
            steps {
                sh '''
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    export PATH="$HOME/.local/bin:$PATH"
                    uv venv
                    uv pip install -r requirements.txt || true
                '''
            }
        }

        stage('Ruff Linter') {
            steps {
                sh 'source .venv/bin/activate && ruff check app'
            }
        }

        stage('Ruff Formatter') {
            steps {
                sh 'source .venv/bin/activate && ruff format --check app'
            }
        }

        stage('Mypy Type Checker') {
            steps {
                sh 'source .venv/bin/activate && mypy app'
            }
        }

        stage('Bandit Security Scanner') {
            steps {
                sh 'source .venv/bin/activate && bandit -r app --exclude .venv --skip B101'
            }
        }

        stage('Safety Dependency Audit') {
            steps {
                sh 'source .venv/bin/activate && safety check'
            }
        }

        stage('Test Coverage') {
            steps {
                sh '''
                    source .venv/bin/activate
                    coverage run -m pytest
                    coverage report --fail-under=80
                    coverage html
                '''
            }
        }
    }

    post {
        success {
            echo '✅ All checks passed!'
        }
        failure {
            echo '❌ One or more checks failed. See stage above.'
        }
    }
}
