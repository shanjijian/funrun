#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mysql.connector import connect

from common.log import log
from core.conf import settings


def initialize_database():
    with connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    ) as conn:
        cursor = conn.cursor()

        # 创建存储函数的表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stored_functions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rule_name VARCHAR(255) UNIQUE NOT NULL,
            function_name VARCHAR(255) UNIQUE NOT NULL,
            function_code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stored_yamls (
            id INT AUTO_INCREMENT PRIMARY KEY,
            rule_name VARCHAR(255) UNIQUE NOT NULL,
            yaml_name VARCHAR(255) UNIQUE NOT NULL,
            yaml_code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        log.info("数据库初始化成功！")


if __name__ == "__main__":
    initialize_database()
