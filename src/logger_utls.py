# -*- coding: utf-8 -*-
# @Date    : 2025-10-19 14:45:29
# @Author  : Lewis Tian (taseikyo@gmail.com)
# @Link    : github.com/taseikyo
# @Version : 3.12.3

import os
from datetime import datetime

from loguru import logger


class Logger:
    def __init__(self, log_dir: str = "log"):
        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)

        # 当天的日志文件名
        log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

        # 移除默认配置，避免重复日志
        logger.remove()

        # 公共格式
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

        # 1) 输出到控制台
        logger.add(
            sink=lambda msg: print(msg, end=""),  # 控制台
            level="INFO",
            format=log_format,
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

        # 2) 输出到文件
        logger.add(
            log_file,
            level="INFO",
            format=log_format,
            rotation="1 day",  # 每天新文件
            retention="7 days",  # 保留 7 天
            encoding="utf-8",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

        self.logger = logger

    def info(self, msg: str):
        self.logger.info(msg)

    def warn(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)
