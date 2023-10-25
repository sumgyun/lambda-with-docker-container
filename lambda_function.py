import json
import subprocess
import pytz
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement

    
    # 현재 시간을 가져옵니다.
    current_time = datetime.now()

    # 타임존을 변경합니다.
    kst_timezone = pytz.timezone('Asia/Seoul')
    current_time_kst = current_time.astimezone(kst_timezone)

    # 변경된 시간을 출력하거나 다른 작업을 수행합니다.
    print("현재 시간 (KST):", current_time_kst)
    
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
