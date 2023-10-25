import json
import subprocess
import wget

def lambda_handler(event, context):
    # TODO implement
    #command = 'ls -l'
    command = 'yum list installed | grep wgrib2'

    # subprocess.run() 함수를 사용하여 명령어 실행
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 실행 결과 출력
    print("표준 출력:", result.stdout.decode())
    print("표준 에러:", result.stderr.decode())
    print("리턴 코드:", result.returncode)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
