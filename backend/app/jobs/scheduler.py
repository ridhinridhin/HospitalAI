from apscheduler.schedulers.background import BackgroundScheduler

from app.jobs.sla_monitor import check_overdue_tickets

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(
        check_overdue_tickets,
        trigger="interval",
        #minutes=30,
        seconds=30,
        id="sla_monitor",
        replace_existing=True,
    )

    scheduler.start()

    print("✅ SLA Scheduler Started")