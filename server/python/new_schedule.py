import schedule


def job():
    print("Added new schedule.")


def add_schedule():
    schedule.every(5).seconds.do(job)
