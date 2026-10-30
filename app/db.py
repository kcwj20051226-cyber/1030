import psycopg2

def get_connection():
    # 請根據你本地 PostgreSQL 的設定修改密碼與資料庫名稱
    conn = psycopg2.connect(
        host="localhost",
        database="activity_db",  # 對應 schema.sql 建立的資料庫名稱
        user="postgres",
        password="0000" # 換成你的 PostgreSQL 密碼
    )
    return conn