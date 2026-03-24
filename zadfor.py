import random
from datetime import datetime
import time
odds = list(range(1,60,2))
right_this_minute = datetime.today().minute
for i in range(5):
    if right_this_minute in odds:
        print("ta minuta jest nieparzysta")
    else:
        print("ta minuta jest parzysta")
    time.sleep(random.randint(1, 60))