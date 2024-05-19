bind = "unix:gunicorn.sock"
workers = 3
raw_env = ["PRODUCTION=True"]
wsgi_app = "lovely.wsgi"
pythonpath = '.venv'