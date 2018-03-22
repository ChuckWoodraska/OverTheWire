import httpimport
import requests
import time

httpimport.INSECURE = True
flag = True

def job():
    print("I'm working...")


with httpimport.github_repo('dbader', 'schedule', 'schedule'):
    import schedule
schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    if flag:
        new_schedule = httpimport.load('new_schedule', 'http://127.0.0.1:5002')
        print(dir(new_schedule))
        new_schedule.add_schedule()
        flag = False
