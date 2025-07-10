pipeline {
    agent any

    tools {
        maven 'Maven'
        jdk 'jdk-17'
    }

    environment {
        SONARQUBE_SERVER = 'Sonar-cve's' // Must match Jenkins config name exactly
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/ahmadk18361/sonar-java-demo-3.git'
            }
        }
        
        stage('Remediate Vulnerabilities') {
            steps {
                bat 'remediation_cve_2020_9488.py'
            }
        }

        stage ('Debug Sonar Token') {
            steps {
                withCredentials([string(credentialsId: '2ndsonar', variable: 'SONAR_TOKEN')]) {
                    bat 'echo Debug: token is %SONAR_TOKEN%'
                }
            }
        }

       stage('Build') {
            steps {
                bat 'mvn clean package'
                bat 'git config --global user.email "jenkins@example.com"'
                bat 'git config --global user.name "Jenkins"'
                bat 'git add .'
                bat 'git commit -m "Apply automatic fix to hardcoded credentials" || exit 0'
                    }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv("${Sonar-cve-s}") {
                    withCredentials([string(credentialsId: '2ndsonar', variable: 'SONAR_TOKEN')]) {
                         bat 'mvn sonar:sonar -Dsonar.token=$SONAR_TOKEN'
                         bat 'echo Sonar token: %SONAR_TOKEN'
                       bat """
                           mvn clean verify sonar:sonar \
                              -Dsonar.projectKey=fix2-scan \
                              -Dsonar.projectName='Sonar-cve's' \
                              -Dsonar.host.url=http://localhost:9000 \
                              -Dsonar.token=sqp_b08b8163f360aa6cb24534b5c579de0a58f6211f

                            """
                    }
                }
            }
        }
    }
}
