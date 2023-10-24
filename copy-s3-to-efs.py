import json
import boto3
import os
import urllib.parse
import subprocess
import logging

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# boto3 S3 client 생성
s3 = boto3.client('s3')

# boto3 EFS client 생성
efs = boto3.client('efs')

# EFS 마운트 포인트 정의
efs_mount_path = '/mnt/lambda/prd/cont/ost'

def lambda_handler(event, context):
    logger.info('=========================================')
    logger.info('image-copy-s3-to-efs 함수 Handler Start')

    # S3 트리거 이벤트에서 버킷명 및 객체 키 저장
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(record['s3']['object']['key'])

    # S3 객체 URL 저장
    s3_object_url = f"s3://{bucket_name}/{object_key}"
    logger.info('S3 object url : %s', s3_object_url)

    # 객체 파일명 저장
    object_name = object_key.split('/')[-1]
    logger.info('S3 object name : %s', object_name)
    tmp_file_url = '/tmp/' + object_name

    # EFS의 target path 정의
    efs_target_path = os.path.join(efs_mount_path, object_key)
    logger.info('EFS target path : %s', efs_target_path)

    # EFS 에 해당 디렉터리 존재여부 체크 -> 미존재시 디렉터리 생성
    efs_dir = os.path.dirname(efs_target_path)
    logger.info(efs_dir)
    if not os.path.exists(efs_dir):
        os.makedirs(efs_dir)
        logger.info('Created directory: %s', efs_dir)

    # 임시파일로 S3 객체 다운로드
    try:
        logger.info('임시파일 객체 다운로드 시작')
        with open(tmp_file_url, 'wb') as data:
            s3.download_fileobj(bucket_name, object_key, data)
            logger.info('임시파일 객체 다운로드 끝')
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error downloading S3 object: {e}')
        }

    # 다운로드 된 객체 EFS로 업로드
    try:
        logger.info('efs 업로드 시작')
        subprocess.run(["cp", tmp_file_url, efs_target_path])
        logger.info('efs 업로드 끝')
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error uploading object to EFS: {e}')
        }

    # 임시파일 삭제
    try:
        os.remove(tmp_file_url)
    except Exception as e:
        logger.error(f'Error deleting tmp file: {e}')

    return {
        'statusCode': 200,
        'body': json.dumps('S3 to EFS file copy completed successfully')
    }
