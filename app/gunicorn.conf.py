# reference: https://docs.gunicorn.org/en/stable/settings.html#
bind = '0.0.0.0:7001'
workers = 8
errorlog = 'gunicorn.log'
capture_output = True
reload = True
