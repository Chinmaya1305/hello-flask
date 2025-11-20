pipeline {
  agent any

  environment {
    IMAGE = "localhost:10090/hello-flask"
    TAG = "latest"
    KIND_CLUSTER = "dev-cluster"
    K8S_MANIFEST_DIR = "k8s"
    WORKDIR = "${env.WORKSPACE}"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Unit Tests (in Docker)') {
      steps {
        // run tests inside an ephemeral Python container so Jenkins host doesn't need Python/Flask installed
        sh '''
          set -e
          echo "Running unit tests inside python:3.10-slim container..."
          docker run --rm -v "${WORKSPACE}":/workspace -w /workspace python:3.10-slim bash -lc "
            pip install --no-cache-dir -r requirements.txt && \
            chmod +x tests/run_tests.sh || true && \
            bash tests/run_tests.sh
          "
        '''
      }
    }

    stage('Build Docker Image') {
      steps {
        sh '''
          set -e
          echo "Building Docker image ${IMAGE}:${TAG}"
          docker build -t ${IMAGE}:${TAG} .
        '''
      }
    }

    stage('Load Image into kind') {
      steps {
        sh '''
          set -e
          echo "Checking if kind cluster exists..."
          if ! kind get clusters | grep -q "^${KIND_CLUSTER}$"; then
            echo "Kind cluster ${KIND_CLUSTER} not found. Creating..."
            kind create cluster --name ${KIND_CLUSTER}
          fi

          echo "Loading Docker image into kind..."
          kind load docker-image ${IMAGE}:${TAG} --name ${KIND_CLUSTER}
        '''
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          set -e
          echo "Applying Kubernetes manifests"
          kubectl apply -f ${K8S_MANIFEST_DIR}/deployment.yaml -f ${K8S_MANIFEST_DIR}/service.yaml

          echo "Waiting for deployment rollout..."
          kubectl rollout status deployment/hello-flask --timeout=120s
        '''
      }
    }
  }

  post {
    success {
      echo "🎉 Pipeline completed successfully!"
    }
    failure {
      echo "❌ Pipeline failed — check console for details."
    }
  }
}

