from datetime import datetime
odds = []
for i in range(60):
    if i % 2 == 1:
        odds.append(i)

right_this_minute = datetime.today().minute

if right_this_minute in odds:
    print("ta minuta jest nieparzysta")
else:
    print("ta minuta jest parzysta")