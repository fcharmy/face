1. cd to face_web folder,   
 update path in nginx.conf and uwsgi.ini, and make sure there is 'log' folder in current folder

2. link conf file to nginx. if existed, open it to check if it works
> sudo ln -s nginx.conf /etc/nginx/sites-enabled/

3. nginx.conf set port to 80, so change nginx default port to others in
> /etc/nginx/sites-enabled/default

4. kill existed port and restart nginx, then see if nginx works in new port
> sudo fuser -k 80/tcp  
> sudo /etc/init.d/nginx restart

5. make migrations of each app
> python3 manage.py makemigrations app_name

6. migrate whole database of django
> python3 manage.py migrate

7. generate static folder 
> python3 manage.py collectstatic

8. cd to this path, run following cmd and open site in browser, then check log file '/var/log/nginx/error.log' if permission denied. if so, '--chmod-socket=664' or 666
> uwsgi --socket face_web.sock --module face_web.wsgi

9. kill port and restart nginx

10. cd to face_web folder and run server
> uwsgi --ini uwsgi.ini
