import json, os
import subprocess
import pytz
from datetime import datetime

def lambda_handler(event, context):
    
    current_time = datetime.now() # currernt time
    kst_timezone = pytz.timezone('Asia/Seoul') # time zone KST
    current_time_kst = current_time.astimezone(kst_timezone)

    print("현재 시간 (UTC):", current_time)
    print("현재 시간 (KST):", current_time_kst)    
 
    #Environment variable
    UTC = 18
    #date = current_time.strftime('%Y%m%d')
    date='20231016'

    for i in range(0, 51):
        num = '{:02d}'.format(i)
        
        download = 'aws s3 cp --no-sign-request s3://noaa-gfs-bdp-pds/gfs.'+date+'/'+str(UTC)+'/atmos/gfs.t'+str(UTC)+'z.pgrb2.0p25.f0'+num+' ./tmp/'
        
        subprocess.run(download, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")

    # /tmp/ 디렉토리 경로
    tmp_dir = '/tmp/'

    # /tmp/ 디렉토리 안에 있는 파일 리스트를 가져옵니다.
    files = os.listdir(tmp_dir)

    # 파일 리스트 출력
    print("Files in /tmp/:")
    for file in files:
        print(file)

    #command = 'ls -l'
    command = 'yum list installed | grep wgrib2'

    # subprocess.run() 함수를 사용하여 명령어 실행
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, executable="/bin/bash")

    # 실행 결과 출력
    print("표준 출력:", result.stdout.decode())
    print("표준 에러:", result.stderr.decode())
    print("리턴 코드:", result.returncode)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
