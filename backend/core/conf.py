#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache


class Settings:
    # DB
    DB_HOST: str = 'localhost'
    DB_PORT: int = 3306
    DB_NAME: str = 'funrun'
    DB_USER: str = 'root'
    DB_PASSWORD: str = 'root'

    # LOG
    LOG_PATH: str = './logs'
    LOG_STDOUT_FILENAME: str = 'funrun_access.log'
    LOG_STDERR_FILENAME: str = 'funrun_error.log'

    # IMPORT
    REQUIRED_LIBRARIES: list = ['requests', 'json', 're']


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
