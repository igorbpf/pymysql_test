import sys
import logging
import rds_config
import pymysql

#rds settings
rds_host = "mysqlforlambdatest.c96nejgzad4f.us-east-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
db_port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name,
                           passwd=password, db=db_name, port=db_port, connect_timeout=60)
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """

    item_count = 0

    with conn.cursor() as cur:
        # cur.execute('drop table if exists Employee;')
        cur.execute('select * from Employee;')
        
        for row in cur.fetchall():
            print(row)

    conn.commit()

    return "Removed RDS MySQL table"


if __name__ == '__main__':
    print(handler('', ''))
