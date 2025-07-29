from app.utils.log_utils import Log


def test_log():
    logger = Log().get_logger()
    logger.info("test")
    logger.debug("test")
    logger.warning("test")
    logger.error("test")
    logger.critical("test")


def test_log2():
    logger = Log().get_logger()
    logger.info("test111")
    logger.debug("test222")
    logger.warning("test333")
