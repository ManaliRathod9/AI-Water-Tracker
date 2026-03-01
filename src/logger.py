import logging

logging.basicConfig(
    filename = "app.log",
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

def log_message(message):
    logging.info(message)

def log_warning(warning):
    logging.warning()
    
def log_error(error):
    logging.error(error)