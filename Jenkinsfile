cat > Jenkinsfile <<'JENFILE'
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

    stage('Setup Python') {
      steps {
        sh '''
          # create venv if missing
          python3 -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          python -m pip install --upgrade pip setuptools wheel
          pip --version
        '''
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          . ${VENV_DIR}/bin/activate
          mkdir -p reports
          echo "PWD: $(pwd)"
          echo "LS root:"
          ls -la
          echo "sys.path preview:"
          python -c "import sys, pprint; pprint.pprint(sys.path[:5])"
          # Ensure workspace root is on PYTHONPATH so tests can import app.py
          PYTHONPATH=. pytest --maxfail=1 --disable-warnings -q --junitxml=reports/junit.xml
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

    stage('Archive Artifacts') {
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
JENFILE
}
