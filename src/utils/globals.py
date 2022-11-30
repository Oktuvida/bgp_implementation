from apscheduler.schedulers.background import BackgroundScheduler


class Globals:
    SCHED = BackgroundScheduler()
    DRAW_TIMER: float = 1
