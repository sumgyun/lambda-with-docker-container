# Define custom function TION_DIR}
ARG FUNCTION_DIR="/function"

FROM python:3.11 as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}

# Install the function's dependencies
RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric

RUN apt-get update && \
    apt-get install -y \
        git \
        build-essential \
        wget \
        cmake \
        gfortran

ENV FC=gfortran
ENV CC=gcc

# Download and build wgrib
RUN wget ftp://ftp.cpc.ncep.noaa.gov/wd51we/wgrib2/wgrib2.tgz.v3.1.3 -O wgrib2.tgz && \
    tar -zxvf wgrib2.tgz && \
    cd grib2 && \
    make lib && \
    mv wgrib2 /usr/local/bin/wgrib2

# Clone the specified GitHub repository
RUN git clone https://github.com/sumgyun/lambda-with-docker-container.git

# Install dependencies from requirements.txt
RUN pip install --target ${FUNTION_DIR} -r ${FUNCTION_DIR}/lambda-with-docker-container/requirements.txt

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
