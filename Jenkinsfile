pipeline {
    agent any

    tools {
        maven 'Maven'
        jdk 'jdk-17'
    }

    environment {
        SONARQUBE_SERVER = 'SonarCloud' // Must match Jenkins config name exactly
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

        stage('Fix SQL Injection') {
            steps {
                bat 'python fix_sql_injection.py'
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
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    withCredentials([string(credentialsId: 'SONAR_TOKEN', variable: 'SONAR_TOKEN')]) {
                       bat """
                            mvn clean compile sonar:sonar \
                              -Dsonar.projectKey=SonarJavaDemo \
                              -Dsonar.projectName='SonarJavaDemo' \
                              -Dsonar.host.url=http://localhost:9000 \
                              -Dsonar.token=sqp_37364ff8c3df723769fa870f1ddfe8cdc0992f89
                            """
                    }
                }
            }
        }
    }
}
