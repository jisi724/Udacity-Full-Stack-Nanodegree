# Project 4 - Catalog APP
Udacity full-stack nano degree project 4 --- Catalog APP

## Before you start
_This is project is build under Vagrant VM, please make sure you have Vagrant VM installed on your device and use **fullstack-nanodegree-vm** repo_

### Get Python2.7
This project is built with Python 2.7, please download and install Python 2.7 in your device from [here](https://www.python.org/downloads/)

### Virtual Box
VirtualBox is the software that actually runs the virtual machine. You can download it from [here](virtualbox.org).

### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from [here](vagrantup.com).

### Prepare VM & Database
All vm configuration and database are in this repo, so just download or clone this repo.

## How to start?
- clone / download this repo
- in your console, cd to this project folder
- run `cd vagrant` to enter the VM folder
- run `vagrant up` to start your VM
- run `vagrant ssh` to login to the VM
- inside the VM, change to catalog directory with `cd /vagrant/catalog`
- run `pip install flask_sqlalchemy` to install necessary lib
- run `python main.py` then you should be able to see the project in `http://localhost:8000/`

## API Usage
This project also provide some baisc API to get category and item infomation.

- `/categories.json`: get all categories.
- `/category/<int:category_id>.json`: get all items under certain category.
- `/items.json`: get all items.
- `/item/<int:item_id>.json`: get specific item by id.

## FAQ
### I have difficulty using Vagrant
please check [Udacity tutorial about Vagrant](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)