from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import atexit

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        atexit.register(self.stop)
        self.tasks = {}

    def add_interval(self, name, func, seconds=60, **kwargs):
        job = self.scheduler.add_job(func, IntervalTrigger(seconds=seconds), id=name, replace_existing=True)
        self.tasks[name] = {"type": "interval", "seconds": seconds}
        print(f"✅ Scheduled: {name} (every {seconds}s)")
        return job

    def add_cron(self, name, func, hour="*", minute="*", **kwargs):
        job = self.scheduler.add_job(func, CronTrigger(hour=hour, minute=minute), id=name, replace_existing=True)
        self.tasks[name] = {"type": "cron", "hour": hour, "minute": minute}
        print(f"✅ Scheduled: {name} (cron {hour}:{minute})")
        return job

    def remove(self, name):
        self.scheduler.remove_job(name)
        self.tasks.pop(name, None)
        print(f"❌ Removed: {name}")

    def list_tasks(self):
        return list(self.tasks.keys())

    def pause(self, name):
        self.scheduler.pause_job(name)

    def resume(self, name):
        self.scheduler.resume_job(name)

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown()

if __name__ == "__main__":
    scheduler = TaskScheduler()
    scheduler.add_interval("test", lambda: print("Running..."), seconds=5)
    print(f"Tasks: {scheduler.list_tasks()}")