pipeline {
  agent { label 'master' }
  environment {
    TARGET_INSTANCE = credentials('target-instance')
    TARGET_CREDENTIALS_ID = credentials('target-credentials-id')
  }
  stages {
    stage('Deploy') {
      steps {
        script {
          docker.withServer("${env.TARGET_INSTANCE}", "${env.TARGET_CREDENTIALS_ID}") {
            sh "docker-compose build"
            sh "docker-compose down"
            sh "docker-compose up -d --force-recreate"
          }
        }
      }
    }
  }
  post {
    always {
      cleanWs()
    }
  }
}
