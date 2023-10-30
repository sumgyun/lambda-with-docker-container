FROM public.ecr.aws/lambda/python:3.8 as lambda-image

# 사용할 환경 : Amazon Linux 2
FROM amazonlinux:2

# 작업 디렉토리 설정
RUN mkdir /var/task
WORKDIR /var/task

# labmda 런타임 이미지 복사
COPY lambda_function.py /var/task/
COPY --from=lambda-image /var/runtime /var/runtime

# python 및 빌드 종속성 설치
RUN amazon-linux-extras install -y python3
RUN yum install -y libgl1-mesa-glx libglib2.0-0 python3-pip

# 추가 패키지 설치
RUN yum install -y git
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y install wgrib

# git clone
RUN git clone https://github.com/sumgyun/lambda-with-docker-container.git

# install packages
RUN pip3 install -r lambda-with-docker-container/requirements.txt

# Lambda Runtime Interface Emulator를 추가하고 보다 간단한 로컬 실행을 위해 ENTRYPOINT에서 스크립트 사용
COPY ./entry_script.sh /entry_script.sh
ADD aws-lambda-rie /usr/local/bin/aws-lambda-rie

RUN chmod 755 /entry_script.sh
RUN chmod 755 /usr/local/bin/aws-lambda-rie

ENTRYPOINT [ "/entry_script.sh" ]

CMD ["lambda_function.lambda_handler"]
