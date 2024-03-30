from apscheduler.schedulers.asyncio import AsyncIOScheduler

from notification_services.src.services.content_reader import NotifyBroker


class Scheduler:

    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def run_every_x_days_job(self):
        n = NotifyBroker()
        n.db_read()
        await n.notify_broker()

    def _add_jobs(self):
        self.scheduler.add_job(self.run_every_x_days_job, 'interval', minutes=1)

    def start_scheduler(self):
        self._add_jobs()
        self.scheduler.start()

    def stop_scheduler(self):
        self.scheduler.shutdown()
