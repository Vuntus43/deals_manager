from deals_manager.settings import *  # noqa
try:
    logger  # noqa
except NameError:
    try:
        from deals_manager.settings import ilogger as logger  # noqa
    except Exception:
        import logging
        logger = logging.getLogger("integration_utils")
