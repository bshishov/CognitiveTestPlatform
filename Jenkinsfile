pipeline {
  agent { label 'master' }
  environment {
    TARGET_INSTANCE = credentials('target-instance')
    TARGET_CREDENTIALS_ID = credentials('target-credentials-id')
    COGNITIVE_DJANGO_HOST = 'test.shishov.me'
    COGNITIVE_LOGS_PATH = '/opt/cognitive/logs'
    COGNITIVE_MEDIA_PATH = '/opt/www/cognitive/media'
    COGNITIVE_MODULES_PATH = '/opt/cognitive/modules'
    COGNITIVE_MYSQL_DATA_CONF = '/opt/cognitive/my.cnf'
    COGNITIVE_MYSQL_DATA_PATH = '/opt/cognitive/mysql'
    COGNITIVE_NETWORK = 'webproxy'
    COGNITIVE_RESULTS_PATH = '/opt/cognitive/results'
    COGNITIVE_STATIC_PATH = '/opt/www/cognitive/static'
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
