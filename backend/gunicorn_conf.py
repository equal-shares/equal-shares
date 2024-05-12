# Configurations for Gunicorn in production

from multiprocessing import cpu_count

# Bind
bind = '127.0.0.1:8000'

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'info'
accesslog = '/app/access_log'
errorlog = '/app/error_log'
