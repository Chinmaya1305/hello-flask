pipeline {
  agent any
  environment {
    ARTIFACTS_PATH = "dist/*.tar.gz"
    VENV_DIR = "venv"
  }
  options {
    timeout(time: 30, unit: 'MINUTES')
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup venv') {
      steps {
        sh '''
          # create venv if missing
          python3 -m venv ${VENV_DIR}
          # ensure pip is available from venv
          . ${VENV_DIR}/bin/activate
          python -m pip install --upgrade pip setuptools wheel
          pip --version
        '''
      }
    }

    stage('Install deps') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          # install into venv (no system packages touched)
          pip install -r requirements.txt
        '''
      }
    }

    stage('Unit tests') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          mkdir -p reports
          pytest --maxfail=1 --disable-warnings -q --junitxml=reports/junit.xml
        '''
      }
      post {
        always {
          junit 'reports/junit.xml'
        }
      }
    }

    stage('Package') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          chmod +x package.sh
          ./package.sh
        '''
      }
    }

    stage('Archive') {
      steps {
        archiveArtifacts artifacts: "${ARTIFACTS_PATH}", fingerprint: true
      }
    }
  }

  post {
    success {
      echo "Pipeline succeeded: build ${env.BUILD_NUMBER}"
    }
    failure {
      echo "Pipeline failed: build ${env.BUILD_NUMBER}"
    }
  }
}

