import os
import time
from datetime import datetime
from config import Config


def log_this(data):
    try_count = 0
    while try_count < 3:
        try:
            now = datetime.now()
            now_string = now.strftime("%Y/%m/%d %H:%M:%S")
            log_folder = Config.LOG_FOLDER
            log_filename = f"{now.strftime('%Y%m%d')}_Mechas.log"
            log_file = os.path.join(log_folder, log_filename)

            with open(log_file, "a+", encoding="utf-8") as log:
                line = f"\n{now_string} {data}"
                log.write(line)
            return
        except:
            try_count += 1
            time.sleep(0.1)
