pipeline {

    agent any

    environment {
        IMAGE = "praveenedward/pydjango"
        TAG   = "v${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE}:${TAG} ./app
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin
                    '''
                }
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    docker push ${IMAGE}:${TAG}
                '''
            }
        }

        stage('Creating Secrets') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'node-db',
                        usernameVariable: 'DB_USER',
                        passwordVariable: 'DB_PASS'
                    ),
		    string(
			credentialsId: 'key',
			variable: 'API_KEY'
		     )
                ]) {
                    sh '''
                        kubectl create secret generic pydjango-secret \
                            --from-literal=DB_USER="$DB_USER" \
                            --from-literal=DB_PASS="$DB_PASS" \
			    --from-literal=API_KEY="$DJANGO_SECRET_KEY" \
                            --dry-run=client -o yaml | kubectl apply -f -
                    '''
                }
            }
        }

        stage('Deploy Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/
                '''
            }
        }

        stage('Update Image') {
            steps {
                sh '''
                    kubectl set image deployment/pydjango-deployment \
                        pydjango=${IMAGE}:${TAG}
                '''
            }
        }

        stage('Rollout Status') {
            steps {
                sh '''
                    kubectl rollout status deployment/pydjango-deployment \
                        --timeout=5m
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment successful: ${IMAGE}:${TAG}"
        }

        failure {
            echo "Deployment failed"
        }
    }
}
