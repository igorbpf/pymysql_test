import os
import sys
import json
import logging
from parser import parse_sql
import boto3
import botocore
import pymysql


#rds settings
rds_host = os.environ.get("HOST", "")
name = os.environ.get("USER", "")
password = os.environ.get("PASSWORD", "")
db_name = os.environ.get("DB_NAME", "")
db_port = int(os.environ.get("PORT", 3306))


# Resource S3
s3 = boto3.resource('s3', region_name='us-east-1',
                    config=botocore.config.Config(s3={'addressing_style': 'path'}))

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, port=db_port, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def handler(event, context):
    """
    This function runs sql scripts in MySQL RDS instance
    """

    bucket_name = os.environ.get('BUCKET_NAME')

    object = s3.Object(bucket_name, key='script/sql_stats.sql')
    file_stream = object.get()['Body'].read()

    print(file_stream)

    stmts = parse_sql(file_stream)

    with conn.cursor() as cur:
        for stmt in stmts:
            cur.execute(stmt)
        conn.commit()

    return json.dumps({'status': 'SQL script successfully submitted'})


if __name__ == '__main__':
    print(handler('', ''))
