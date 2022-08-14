import logging
from datetime import datetime
import os


LOG_DIR = "insurance_logs"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S') }"
LOG_FILE_NAME = F"log_{CURRENT_TIME_STAMP}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)


os.makedirs(LOG_DIR,exist_ok=True)
logging.basicConfig(filename=LOG_FILE_PATH,
                level=logging.INFO,
                filemode="w",
                format= "[%(asctime)s---%(name)s] %(module)s (%(levelname)s)  ===> %(message)s")