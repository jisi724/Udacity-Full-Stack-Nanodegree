# UC_FSNano_3_Log_Analysis
Udacity full-stack nano degree project 3 --- Log Analysis

## Before you start
_This is project is build under Vagrant VM, please make sure you have Vagrant VM installed on your device and use **FSND-Virtual-Machine**_

### Get Python2.7
This project is built with Python 2.7, please download and install Python 2.7 in your device from [here](https://www.python.org/downloads/)

### Virtual Box
VirtualBox is the software that actually runs the virtual machine. You can download it from [here](virtualbox.org).

### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from [here](vagrantup.com).

### Prepare VM & Database
To properly config your Vagrant VM, you can download the [FSND-VM.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) provided by Udacity.
Then find a folder named `vagrant` from the downloaded folder. We will use this folder later.
Download database provided by Udacity from [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip it and put the `newsdata.sql` in to the `vagrant` directory.

## How to start?
- cd into your vagrant directory
- run `vagrant up` to start your VM
- run `vagrant ssh` to log into the VM
- inside the VM, change directory to `/vagrant`
- run `psql -d news -f newsdata.sql` to load data to database
- clone or download the project into current vagrant folder, then cd into the project's directory
- run `psql news` to connect news database, then run following 2 scripts to create necessary views

### Create views before running the script
**VIEW: view_error**
```sql
CREATE VIEW view_error AS
SELECT count(*) AS num_of_requests, time::timestamp::date as date
FROM log
WHERE status != '200 OK'
GROUP BY time::timestamp::date;
```

**VIEW: view_total**
```sql
CREATE VIEW view_total AS
SELECT count(*) AS num_of_requests, time::timestamp::date as date
FROM log
GROUP BY time::timestamp::date;
```

- run `\q` to exit psql prompt
- run `python logs_analysis.py` to see the result


## FAQ
### I have difficulty using Vagrant
please check [Udacity tutorial about Vagrant](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)

### I have difficulty using psql and creating view?
please check Udacity tutorial about Database.