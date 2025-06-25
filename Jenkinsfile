pipeline {
    agent any

    environment {
        PATH = "${HOME}/.local/bin:${PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Env') {
            steps {
                sh '''
                    curl -LsSf https://astral.sh/uv/install.sh | sh
                    export PATH="$HOME/.local/bin:$PATH"
                    uv venv
                    uv sync
                '''
            }
        }

        stage('Ruff Linter') {
            steps {
                sh '''
                    . .venv/bin/activate
                    ruff check .
                '''
            }
        }

        stage('Ruff Formatter') {
            steps {
                sh '''
                    . .venv/bin/activate
                    ruff format .
                '''
            }
        }

        stage('Mypy Type Checker') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mypy --ignore-missing-imports --scripts-are-modules .
                '''
            }
        }

        stage('Bandit Security Scanner') {
            steps {
                sh '''
                    . .venv/bin/activate
                    bandit --recursive --exclude $WORKSPACE/.venv,$WORKSPACE/.coverage,$WORKSPACE/.pytest_cache --skip B101 $WORKSPACE
                '''
            }
        }

        stage('Safety Dependency Audit') {
            steps {
                sh '''
                    . .venv/bin/activate
                    safety check --full-report --file pyproject.toml
                '''
            }
        }

        stage('Test Coverage') {
            steps {
                sh '''
                    . .venv/bin/activate
                    uv pip install pytest pytest-cov
                    pytest --cov=.
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ One or more checks failed. See stage above.'
        }
        success {
            echo '✅ All checks passed successfully.'
        }
    }
}
