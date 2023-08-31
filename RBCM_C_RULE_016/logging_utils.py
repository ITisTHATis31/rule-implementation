import logging

def setup_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

def get_logger(name):
    return logging.getLogger(name)

def log_info(logger, rule_name, rule_info):
    logger.info("==============================================================================================================================")
    # Log the rule name and the rule information
    logger.info("#"*75)
    logger.info(f" Rule : {rule_name}, Rule Info : {rule_info}")
    logger.info(f"#"*75)
