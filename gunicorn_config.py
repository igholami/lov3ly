bind = "0.0.0.0:8000"
workers = 3
raw_env = ["PRODUCTION=True"]
wsgi_app = "lovely.wsgi"
pythonpath = '.venv'