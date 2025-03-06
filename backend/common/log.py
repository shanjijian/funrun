#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from loguru import logger
from backend.core.conf import settings


class Logger:
    def __init__(self):
        self.log_path: str = settings.LOG_PATH
        os.makedirs(self.log_path, exist_ok=True)

    def log(self) -> logger:
        # 日志文件路径
        log_stdout_file: str = os.path.join(self.log_path, settings.LOG_STDOUT_FILENAME)
        log_stderr_file: str = os.path.join(self.log_path, settings.LOG_STDERR_FILENAME)

        log_config = dict(rotation='10 MB', retention='30 days', compression='tar.gz', enqueue=True)

        # 配置日志处理器
        logger.add(
            log_stdout_file,
            level='INFO',
            filter=lambda record: record['level'].name == 'INFO' or record['level'].no <= 25,
            **log_config,
            backtrace=False,
            diagnose=False,
        )
        logger.add(
            log_stderr_file,
            level='ERROR',
            filter=lambda record: record['level'].name == 'ERROR' or record['level'].no >= 30,
            **log_config,
            backtrace=True,
            diagnose=True,
        )

        return logger


log = Logger().log()
