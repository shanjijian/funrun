from mysql.connector import connect, Error
from typing import Optional, Dict, List
from backend.common.log import log
from backend.core.conf import settings


class BaseDAO:
    """数据库操作基类"""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.conn_params = {
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "database": settings.DB_NAME
        }

    def _get_connection(self):
        """获取数据库连接"""
        try:
            return connect(**self.conn_params)
        except Error as e:
            log.error(f"数据库连接失败: {e}")
            raise

    def _execute_write(self, query: str, params: tuple) -> bool:
        """执行写操作通用方法"""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount > 0
            except Error as e:
                log.error(f"操作失败: {e}")
                conn.rollback()
                return False

    def _execute_read(self, query: str, params: tuple = None) -> List[Dict]:
        """执行读操作通用方法"""
        with self._get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            return cursor.fetchall()
        