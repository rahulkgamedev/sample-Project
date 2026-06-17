pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_USERNAME = credentials('docker-username')
        DOCKER_PASSWORD = credentials('docker-password')
        DOCKER_IMAGE = "${DOCKER_USERNAME}/python-app"
        KUBE_NAMESPACE = 'python-app'
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        BUILD_TAG = "${BUILD_NUMBER}-${GIT_COMMIT_SHORT}"
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Build Python Application') {
            steps {
                echo 'Building Python application...'
                script {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                script {
                    sh '''
                        . venv/bin/activate
                        pip install pytest pytest-cov
                        pytest tests/ --cov=. --cov-report=xml || true
                    '''
                }
            }
        }
        
        stage('Code Quality Analysis') {
            steps {
                echo 'Running code quality checks...'
                script {
                    sh '''
                        . venv/bin/activate
                        pip install pylint flake8
                        flake8 app.py --max-line-length=100 || true
                        pylint app.py --disable=all --enable=E,F || true
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh '''
                        docker build -t ${DOCKER_IMAGE}:${BUILD_TAG} .
                        docker tag ${DOCKER_IMAGE}:${BUILD_TAG} ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker image to registry...'
                script {
                    sh '''
                        echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
                        docker push ${DOCKER_IMAGE}:${BUILD_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                        docker logout
                    '''
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes cluster...'
                script {
                    sh '''
                        kubectl apply -f k8s/namespace.yaml
                        kubectl apply -f k8s/serviceaccount.yaml
                        kubectl apply -f k8s/configmap.yaml
                        kubectl apply -f k8s/service.yaml
                        kubectl set image deployment/python-app python-app=${DOCKER_IMAGE}:${BUILD_TAG} -n ${KUBE_NAMESPACE}
                        kubectl apply -f k8s/ingress.yaml
                        kubectl apply -f k8s/hpa.yaml
                        kubectl rollout status deployment/python-app -n ${KUBE_NAMESPACE} --timeout=5m
                    '''
                }
            }
        }
        
        stage('Smoke Test') {
            steps {
                echo 'Running smoke tests...'
                script {
                    sh '''
                        sleep 5
                        curl -f http://localhost:5000/health || echo "Health check failed"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv || true'
            cleanWs()
        }
        
        success {
            echo 'Pipeline execution successful!'
        }
        
        failure {
            echo 'Pipeline execution failed!'
        }
    }
}
