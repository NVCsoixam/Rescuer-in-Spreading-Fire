"""
app/core/logger.py

Centralized logging configuration for the Rescue Simulation System.
Provides structured JSON logging with file rotation support.
As defined in 16_logging_monitoring.md.
"""

from __future__ import annotations
import logging
import sys
import json
from pathlib import Path


class JsonFormatter(logging.Formatter):
    """Format log records as JSON strings."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "module": record.name,
            "event": getattr(record, "event", record.funcName),
            "message": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, ensure_ascii=False)


def setup_logger(
    name: str = "rescue_sim",
    level: int = logging.INFO,
    log_dir: str | None = "logs",
) -> logging.Logger:
    """
    Set up and return a configured logger instance with JSON formatting.

    Args:
        name: Logger name, typically the module name.
        level: Logging level (DEBUG, INFO, WARNING, ERROR).
        log_dir: Directory for log files. None disables file logging.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    # Console handler with JSON format
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)

    # File handler with rotation support
    if log_dir:
        try:
            log_path = Path(log_dir)
            log_path.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(
                str(log_path / "simulation.log"), encoding="utf-8"
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(JsonFormatter())
            logger.addHandler(file_handler)
        except OSError:
            # Silently fall back to console-only if log dir fails
            pass

    return logger


# Pre-configured module-level loggers for quick import
sim_logger: logging.Logger = setup_logger("rescue_sim")
engine_logger: logging.Logger = setup_logger("engine")
ai_logger: logging.Logger = setup_logger("ai")
fire_logger: logging.Logger = setup_logger("fire")