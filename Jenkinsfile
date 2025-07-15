pipeline {
    agent any

    tools {
        maven 'Maven'
        jdk 'jdk-17'
    }

    environment {
        SONARQUBE_SERVER = 'Sonar-cve's' // Must match Jenkins config name exactly
    }

    stage('Checkout') {
          steps {
            checkout([$class: 'GitSCM',
              branches: [[name: '*/main']],
              userRemoteConfigs: [[url: 'https://github.com/ahmadk18361/sonar-java-demo-3.git']],
              extensions: [[$class: 'CloneOption', noTags: false, shallow: false, depth: 0]]
            ])
          }
        }
        
    stage('Remediate Vulnerabilities') {
        steps {
            bat 'remediation_cve_2020_9488.py src/main/java/com/example/Log4jBufferedInputExample.java'
            bat 'remediation_cve_2020_9488.py src/main/java/com/example/Log4jCVE2020_9488Example.java'
            bat 'remediation_cve_2020_9488.py src/main/java/com/example/Log4jCmdArgsExample.java'
            }
        }

     stage('Git Commit Remediated Files') {
        steps {
            dir('project2') {
                bat 'git config --global user.email "scanner@example.com"'
                bat 'git config --global user.name "CVE Scanner Bot"'
                bat 'git add src/main/java/com/example/'
                bat 'git commit -m "Committing all remediated CVE Java files" || echo "Nothing to commit"'
            }
        }
     }
     
        stage ('Debug Sonar Token') {
            steps {
                withCredentials([string(credentialsId: '2ndsonar', variable: 'SONAR_TOKEN')]) {
                    bat 'echo Debug: token is %SONAR_TOKEN%'
                }
            }
        }

        stage( 'Buildwith Maven')
            steps {
                bat 'mvn clean packages'
            }
        
        
        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv("${Sonar-cve-s}") {
                    withCredentials([string(credentialsId: '2ndsonar', variable: 'SONAR_TOKEN')]) {
                         bat 'mvn sonar:sonar -Dsonar.token=$SONAR_TOKEN'
                         bat 'echo Sonar token: %SONAR_TOKEN'
                       bat """
                           mvn clean verify sonar:sonar \
                              -Dsonar.projectKey=sonar-cve-fix2 \
                              -Dsonar.projectName='sonar-cve-fix2' \
                              -Dsonar.host.url=http://localhost:9000 \
                              -Dsonar.sources=src/main/java/com/example
                              -Dsonar.token=sqp_71048fedece31660d5d4ad8c814ec2e490d28c3c
                            """
                    }
                }
            }
        }
    }


