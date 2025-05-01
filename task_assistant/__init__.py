import logging, sys
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)s  %(levelname)s ▸ %(message)s",
    stream=sys.stdout,
)

__version__ = '0.0.0'
