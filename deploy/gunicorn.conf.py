# Listen to internal network ports
bind = '0.0.0.0:8001'

# Work directory
chdir = '/fba/backend/app'

# Concurrency Level
workers = 1

# Specify the number of threads for each worker.
threads = 4

# Monitor
backlog = 512

# Timeout
timeout = 120

# Set the guardian process.,Give the process to supervisor Management; If set to True time,supervisor Startup log is.: 
# gave up: fastapi_server entered FATAL state, too many start retries too quickly
# then it needs to be changed to: False
daemon = False

# Work mode coroutine
worker_class = 'uvicorn.workers.UvicornWorker'

# Set maximum concurrency.
worker_connections = 2000

# Set process file directory
pidfile = '/fba/gunicorn.pid'

# Set access log and error log paths.
accesslog = '/var/log/fastapi_server/gunicorn_access.log'
errorlog = '/var/log/fastapi_server/gunicorn_error.log'

# Set this value totrue only
capture_output = True

# Set log recording level.
loglevel = 'debug'

# pythonProgram
pythonpath = '/usr/local/lib/python3.10/site-packages'

# Start gunicorn -c gunicorn.conf.py main:app
