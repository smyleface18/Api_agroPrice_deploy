from apscheduler.schedulers.background import BackgroundScheduler;
from task import dowload_save;





cron_dowload_save = BackgroundScheduler();



   
cron_dowload_save.add_job(dowload_save, 'interval', seconds = 30)


