# aws 에서 제공하는 lambda base image (python)
FROM amazon/aws-lambda-python:3.9

# optional : ensure that pip is up to data
RUN /var/lang/bin/python3.9 -m pip install --upgrade pip

# install git 
RUN yum install git -y

# install epel-release, wgrib2
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y install wgrib

# 현재 디렉토리의 wgrib 파일을 Lambda 레이어에 추가
COPY ./wgrib2 /var/task/
RUN chmod +x /var/task/wgrib2

# git clone
RUN git clone https://github.com/sumgyun/lambda-with-docker-container.git

# install packages
RUN pip install -r lambda-with-docker-container/requirements.txt

# git repository 의 lambda_function.py 를 Container 내부의 /var/task/ 로 이동
RUN cp lambda-with-docker-container/lambda_function.py /var/task/

# lambda_function.handler 실행
CMD ["lambda_function.lambda_handler"]
