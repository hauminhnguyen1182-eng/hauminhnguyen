import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

LOG_DIR = "/workspace/logs"
os.makedirs(LOG_DIR, exist_ok=True)

class AppLogger:
    def __init__(self, name="mimocode", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            # Console
            console = logging.StreamHandler()
            console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
            self.logger.addHandler(console)

            # File
            file_handler = RotatingFileHandler(
                f"{LOG_DIR}/{name}.log", maxBytes=5*1024*1024, backupCount=3
            )
            file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
            self.logger.addHandler(file_handler)

    def info(self, msg): self.logger.info(msg)
    def error(self, msg): self.logger.error(msg)
    def warning(self, msg): self.logger.warning(msg)
    def debug(self, msg): self.logger.debug(msg)

    def task_start(self, task_name):
        self.info(f"▶ Task started: {task_name}")

    def task_done(self, task_name):
        self.info(f"✓ Task completed: {task_name}")

    def task_error(self, task_name, error):
        self.error(f"✗ Task failed: {task_name} - {error}")

if __name__ == "__main__":
    log = AppLogger()
    log.info("Logger test")
    log.task_start("test_task")
    log.task_done("test_task")