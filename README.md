# Dev mode
- create virtualenv
- install packages from requirements.txt
- run migrations
- run `python manage.py runserver`

# Production deploy mode
To run app in production follow steps described here:
https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-debian-8

## Notice:
if you use debian minimal installation and `usermod` command not working, use `/usr/sbin/usermod` instead

### config files used:

`/etc/nginx/sites-enabled/eshop`
```
server {
    listen 80;
    server_name eshop.test;

    location /static/ {
        root /home/lexx/eshop/;
    }
    location / {
	include         uwsgi_params;
	uwsgi_pass      unix:/tmp/uwsgi-eshop.sock;
    }
} 
```


`/etc/uwsgi/apps-enabled/eshop.ini`
```
[uwsgi]
project = eshop
uid = lexx
base = /home/%(uid)

chdir = %(base)/%(project)
home = %(base)/Env/%(project)
module = config.wsgi:application
plugins = python37
master = true
processes = 5
# socket = /run/uwsgi/%(project).sock
socket = /tmp/uwsgi-%(project).sock
chown-socket = %(uid):www-data
chmod-socket = 660
vacuum = true
```

`/etc/uwsgi/emperor.ini`
```
[uwsgi]
emperor = /etc/uwsgi/apps-enabled
uid = www-data
gid = www-data
limit-as = 1024
logto = /tmp/uwsgi.log
```

If uwsgi.service is not working, start uwsgi in emperor mode as following:
`uwsgi --ini /etc/uwsgi/emperor.ini &`

Be careful to name both venv and project folders with the same name!
