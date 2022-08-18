import logging
from datetime import datetime
import os
import pandas as pd


# LOG_DIR = "insurance_logs"
# CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S') }"
# LOG_FILE_NAME = F"log_{CURRENT_TIME_STAMP}.log"
# LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)


# os.makedirs(LOG_DIR,exist_ok=True)
# logging.basicConfig(filename=LOG_FILE_PATH,
#                 level=logging.INFO,
#                 filemode="w",
#                 format= "[%(asctime)s---%(name)s] %(module)s (%(levelname)s)  ===> %(message)s")

LOG_DIR="logs"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S') }"
def get_log_file_name():
    return f"log_{CURRENT_TIME_STAMP}.log"

LOG_FILE_NAME=get_log_file_name()

os.makedirs(LOG_DIR,exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE_NAME)



logging.basicConfig(filename=LOG_FILE_PATH,
filemode="w",
format='[%(asctime)s]^;%(name)s;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
level=logging.INFO
)

def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]
