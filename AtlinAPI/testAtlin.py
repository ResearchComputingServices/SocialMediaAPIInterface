from AtlinAPI import *

atlin = AtlinYoutube("http://localhost:5000")
jobs = atlin.get_jobs()

job_uid = 123456789
atlin.set_job_status(job_uid, JobStatus().running)

#TODO put operation
# http://localhost:5000/api/v1/jobs/123456789
# data = {"job_status": "JOB_STATUS"}

#TODO set_quota
#TODO update_job