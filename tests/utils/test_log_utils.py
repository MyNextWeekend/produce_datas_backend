from app.utils.log_utils import Log


def test_log():
    logger = Log().get_logger()
    logger.info("test")
    logger.debug("test")
    logger.warning("test")
    logger.error("test")
    logger.critical("test")
