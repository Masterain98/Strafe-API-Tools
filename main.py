# -*-coding:UTF-8-*-
import time
import datetime

import strafeRequest
from config import cycleTime


# Get Task queue
task1 = datetime.datetime.now()
task2 = task1 + datetime.timedelta(hours=24)
task3 = task1 + datetime.timedelta(hours=48)
# Reformat the datetime
task1 = task1.strftime("%Y-%m-%d")
task2 = task2.strftime("%Y-%m-%d")
task3 = task3.strftime("%Y-%m-%d")

# Daemon
if cycleTime != 0:
    while cycleTime != 0:
        strafeRequest.taskQueue(task1)
        strafeRequest.taskQueue(task2)
        strafeRequest.taskQueue(task3)
        time.sleep(cycleTime)
        print("Waiting for next task cycle:", cycleTime, "seconds")
else:
    strafeRequest.taskQueue(task1)
    strafeRequest.taskQueue(task2)
    strafeRequest.taskQueue(task3)