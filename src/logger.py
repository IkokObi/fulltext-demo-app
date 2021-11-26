import logging


def setup_logger(name, level):
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        """ レンダリングの関係で複数回実行されるため、初回のみhandlerを設定する """
        logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler_format = logging.Formatter(
            fmt="%(levelname)s %(asctime)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
        handler.setFormatter(handler_format)
        logger.addHandler(handler)
        logger.propagate = False
    return logger
