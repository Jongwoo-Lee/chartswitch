
import logging
import sys

LOGGING_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(funcName)s : %(message)s"

def configure_logging(production_mode=False):

    # Configure the logging system
    logging.basicConfig(
        format= LOGGING_FORMAT,
        filename="app.log",
        filemode="a"
    )

    # Create a custom logger
    logger = logging.getLogger("chartswitch")
    
    # Clear any existing handlers (useful in Jupyter notebooks or interactive environments)
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Set the logging level based on the mode
    if production_mode:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    
    # Create console handler with Level INFO
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter and add it to the console handler
    formatter = logging.Formatter(LOGGING_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add the console handler to the logger
    logger.addHandler(console_handler)

# Create a custom logger
logger = logging.getLogger("chartswitch")