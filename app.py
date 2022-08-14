from insurance.logger import logging
from insurance.exception import InsuranceException
import sys

if __name__ == "__main__":
    logging.info("testing the logging module")

    try:
        raise Exception("testing the exeception module")
    
    except Exception as e:
        insurance =  InsuranceException(e,sys)
        logging.exception(insurance.error_message)