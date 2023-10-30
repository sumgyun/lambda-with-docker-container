import json, os
import boto3
from datetime import datetime
import subprocess

def lambda_handler(event, context):

    command = 'echo "Hello, Lambda!"'

    # subprocess를 사용하여 명령 실행
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # 결과 출력
    print(f"명령 실행 결과 코드: {result.returncode}")
    print(f"표준 출력:\n{result.stdout}")
    print(f"표준 에러:\n{result.stderr}")
    
    current_time = datetime.now() # currernt time
    print("현재 시간 (UTC):", current_time)
 
    #Environment variable
    UTC = 18
    #date = current_time.strftime('%Y%m%d')
    date='20231016'
    cycle_18 = 2
    wgrib2_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'wgrib2') # wgrib2 exe path 
    
    s3 = boto3.client('s3')
    aws_gfs_bucket = 'noaa-gfs-bdp-pds' # NOAA Global Forecast System (GFS)
    datalake_bucket = 'cf-templates-12s7rta9jx4zs-us-east-1' # example

    for i in range(0, cycle_18):
        num = '{:02d}'.format(i)
        tmp_dir = '/tmp/'

        object_name = 'gfs.'+date+'/'+str(UTC)+'/atmos/gfs.t'+str(UTC)+'z.pgrb2.0p25.f0'+num
        file_name = 'gfs.t'+str(UTC)+'z.pgrb2.0p25.f0'+num
        s3.download_file(aws_gfs_bucket, object_name, tmp_dir+file_name)

        wgrib_file_name = 'gfs.0p25.'+date+str(UTC)+'.f0'+num+'.grib2'
        #command = 'wgrib2 '+file_name+' -small_grib 123:132 30:40 '+wgrib_file_name
        #command = ['/usr/local/bin/wgrib2', f'{wgrib2_path} '+file_name+' -small_grib 123:132 30:40 '+wgrib_file_name]
        #command = ['/var/task/wgrib2', file_name, '-small_grib', '123:132', '30:40', wgrib_file_name]
        command = ["which", "wgrib2"]

        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        s3.upload_file(tmp_dir+wgrib_file_name, datalake_bucket, wgrib_file_name)
        os.remove(tmp_dir+file_name)
  
    files = os.listdir('/tmp/')
    print("Files in /tmp/:")
    for file in files:
        print(file)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
