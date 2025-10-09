from celery import Celery
from app.config import settings

# Create Celery app
celery_app = Celery(
    "healthify",
    broker=f"mongodb://{settings.mongo_url.split('://')[1]}/celery_broker",
    backend=f"mongodb://{settings.mongo_url.split('://')[1]}/celery_backend",
    include=["app.tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Periodic tasks
celery_app.conf.beat_schedule = {
    "cleanup-expired-sessions": {
        "task": "app.tasks.cleanup_expired_sessions",
        "schedule": 3600.0,  # Run every hour
    },
    "send-reminder-emails": {
        "task": "app.tasks.send_reminder_emails",
        "schedule": 86400.0,  # Run daily
    },
}

if __name__ == "__main__":
    celery_app.start()
