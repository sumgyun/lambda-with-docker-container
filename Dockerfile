# Define custom function directory
ARG FUNCTION_DIR="/function"

FROM python:3.11 as build-image

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  git

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}

# Install the function's dependencies
RUN pip install -m pip install \
    --target ${FUNCTION_DIR} \
    --no-cache-dir \
        awslambdaric \
    -r ${FUNCTION_DIR}/requirements.txt

# Git Clone
RUN git clone https://github.com/sumgyun/lambda-with-docker-container.git

# Unstall epel-release
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-lastest-7.roarch.rpm

# Install wgrib
RUN yum install -y wgrib

# Use a slim version of the base Python image to reduce the final image size
FROM python:3.11-slim

# Include global arg in this stage of the build
ARG FUNCTION_DIR
# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set runtime interface client as default command for the container runtime
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
# Pass the name of the function handler as an argument to the runtime
CMD [ "lambda_function.lambda_handler" ]
