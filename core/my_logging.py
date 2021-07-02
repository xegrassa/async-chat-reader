import logging


def configure_logging(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(levelname)s:%(module)s:%(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)
