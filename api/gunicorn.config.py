import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 600
max_requests = 1000
max_requests_jitter = 50
log_file = '-'