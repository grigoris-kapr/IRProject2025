Build the Docker images:

Base image for Spark NLP:

`docker build -f Dockerfile.spark -t spark-runtime .`

Development image from base image that installs python dependencies:

`docker build -f Dockerfile.dev -t spark-nlp-dev .`

Runs the backend server:

`uvicorn src.backend:app --reload`