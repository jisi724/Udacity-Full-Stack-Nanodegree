# UC_FSNano_6_Linux_Server

Udacity full-stack nano degree assignment 6

_This project is to take a baseline installation of a Linux server and prepare it to host previous catalog python project. The AWS services lightsail and route 53 been used as host and DNS tool. Also, PostgreSQL been chosen as the database._

- IP Address: 18.237.0.154
- SSH Port: 2200
- Web Application URL: http://udacity-linux.runhangz.com/
- SSH to server: `ssh grader@udacity-linux.runhangz.com -p 2200 -i ~/.ssh/privateKeyName`



## Summary of details

### 1. Secure your server.

**Update all currently installed packages.**

```shell
$ sudo apt-get update
$ sudo apt-get upgrade
```

**Change the SSH port from 22 to 2200**

update `/etc/ssh/sshd_config` through `vim `, change port to 2200.

**Configure the UFW to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).**

```shell
# check status and disable ufw first
$ sudo ufw status
$ sudo ufw disable

# setup default rules
$ sudo ufw default deny incoming
$ sudo ufw default allow outgoing

# setup custom rules
$ sudo ufw allow 2200/tcp
$ sudo ufw allow www
$ sudo ufw allow 123/udp

# enable ufw
$ sudo ufw enable
```



### 2. Give `grader` access.

```shell
# Create a new user account named grader.
$ sudo adduser grader

# Give grader the permission to sudo. 
$ sudo vim /etc/sudoers.d/grader
# add: grader ALL=(ALL) NOPASSWD:ALL

# Create an SSH key pair for grader
# first, generate ssh key locally
$ sudo su - grader
$ mkdir ~/.ssh
$ chmod 700 ~/.ssh
$ vim ~/.ssh/authorized_keys
# add: paste generated public key to authorized_keys
$ chmod 644 .ssh/authorized_keys
```



### 3. Prepare to deploy your project.

**Configure the local timezone to UTC**

`sudo dpkg-reconfigure tzdata` then choose none -> UTC

**Install and configure Apache to serve a Python mod_wsgi application.**

```shell
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi
$ sudo service apache2 restart
```

**Install and configure PostgreSQL**

```shell
$ sudo apt-get install postgresql psycopg2
$ sudo su - postgres
$ psql
postgres=# CREATE DATABASE catalog;
postgres=# CREATE USER catalog;
postgres=# ALTER ROLE catalog WITH PASSWORD 'udacity';
postgres=# GRANT ALL PRIVILEGES ON DATABASE catalog TO catalog;
postgres=# \q
```

**Install `git`**

Git has been installed by lightsail ubuntu os.



### 4. Deploy the Item Catalog project.

First, prepare the python environment and clone the project.

```shell
# install python 2.7 and pip
$ sudo apt-get install python2.7 pip

# clone app from github
$ cd /var/www
$ sudo mkdir Catalog
$ cd Catelog
$ sudo git clone https://github.com/jisi724/UC_FSNano_4_Catalog_APP.git .

# reslove error "unsupported locale setting"
$ export LC_ALL="en_US.UTF-8"
$ export LC_CTYPE="en_US.UTF-8"

# install virtual environment
$ sudo pip install virtualenv
$ sudo virtualenv catalog
$ sudo source catalog/bin/activate

# install flask and corresponding dependencies
$ sudo pip install Flask flask_sqlalchemy oauth2client requests

# rename main.py to __init__.py
$ sudo mv main.py __init__.py
```

Then, configure and enable a new Virtual Host

Create a new conf file by `$ sudo vim /etc/apache2/sites-available/Catalog.conf`

Add following content

```
<VirtualHost *:80>
		ServerName udacity-linux.runhangz.com
		ServerAdmin ethan@skyrocket.is
		WSGIScriptAlias / /var/www/Catalog/vagrant/catalog.wsgi
		<Directory /var/www/Catalog/vagrant/catalog/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/Catalog/vagrant/catalog/static
		<Directory /var/www/Catalog/vagrant/catalog/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Next step is to create the .wsgi file, run `sudo vim /var/www/Catalog/vagrant/catalog.wsgi`, and add following content into it:

```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Catalog/vagrant/")

from catalog import app as application
application.secret_key = 'My Secret key'
```

Restart the Apache server by `sudo service apache2 restart`

now you can see the APP running with original SQLite database on the domain.

**Issues met here**

- Google OAuth was not working properly because the new domain needs to be added to Google API Console. Add the new Authorised JavaScript origins resolved the issue.
- The `client_secrets.json` also need to be updated.
- The relative path of `client_secrets.json` returns an error that cannot find the file. Changing it to the absolute path `/var/www/Catalog/vagrant/catalog/client_secrets.json` resloved the issue.



### 5. Plug App to PostgreSQL database

Since we need to replace the SQLite with PostgreSQL, the database connection needs to be updates.

update `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catelogs.db'` to `app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://catalog:udacity@localhost/catalog'` in `__init__.py`, `models.py` and `fake_db_data.py`

- catalog: username
- udacity: password
- localhost/catalog: database name

then run `sudo python fake_db_data.py` to init the database schema and fill in some sample data. 

now the app is running with PostgreSQL database.

**Issues met here**

- According to the warning, `psycopg2-binary` needs to be installed rather the `psycopg2` to init the database schema.
- According to the error message, add `app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True` to the `fake_db_data.py`



## Reference

- [How To Secure PostgreSQL on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-secure-postgresql-on-an-ubuntu-vps)
- [PostgreSQL Basics by Example](https://blog.trackets.com/2013/08/19/postgresql-basics-by-example.html)
- [How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

