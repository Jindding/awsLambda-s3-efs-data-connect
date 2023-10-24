import json
import boto3
import os
import urllib.parse
import subprocess
import logging

# boto3 s3 client 생성
s3 = boto3.client('s3')

# boto3 efs client 생성
efs = boto3.client('efs')

# EFS 마운트 포인트 정의
efs_mount_path = '/mnt/lambda/prd/cont/ost'

# 로깅 설정
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    # event 정보에 대한 검증로직, s3 trigger 로 호출되는 Lambda 함수이기 때문에 굳이 필요없을 것 같아 주석처리..
    # if not record or 's3' not in record or 'bucket' not in record['s3'] or 'name' not in record['s3']['bucket']:
    #     return {
    #         'statusCode': 400,
    #         'body': json.dumps('Invalid input: s3 bucket name is null or missing')
    #     }
    # if 'object' not in record['s3'] or 'key' not in record['s3']['object']:
    #     return {
    #         'statusCode': 400,
    #         'body': json.dumps('Invalid input: s3 object key is null or missing')
    #     }

    # S3 트리거 이벤트에서 버킷명 및 객체 키 저장
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(record['s3']['object']['key'])

    # EFS 마운트 포인트와 파일 경로 생성
    efs_target_path = os.path.join(efs_mount_path, object_key)
    print('efs_타겟 경로 : ')
    print(efs_target_path)

    # EFS 데이터 삭제
    try:
        result = subprocess.run(["rm", '-rf', efs_target_path], capture_output=True, text=True)
        logger.info('EFS file remove complete. Output: %s', result.stdout)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error deleting EFS file: {e}')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('EFS file deletion completed successfully')
    }