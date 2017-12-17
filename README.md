# backend-tests

## Set the settings

Create test database by sql-queries:

	> CREATE DATABASE `test` CHARACTER SET utf8 COLLATE utf8_general_ci;
	> GRANT ALL PRIVILEGES ON test.* TO 'freehackquest_u'@'localhost' WITH GRANT OPTION;
	> FLUSH PRIVILEGES;

Change the name of the database for the tests in file /etc/freehackquest-backend/conf.ini

	name=test

And if not exists test account "admin" with password "admin" then change setings for connection in file backend-tests/classbook/lib.py

## Requirements

Tests are only run with python 3.6.
Install pytest

	$ sudo apt install python-pip
	$ pip3 install -U pytest
	$ pip3 install websocket-client PyMySQL

## Run tests

Check work freehackquestbackend and mysql.
Download repo and change directory to repo.

	$ git clone https://github.com/freehackquest/backend-tests.git
	$ cd ./backend-tests
	$ pytest

## After tests

Change the name of the database for the production in file /etc/freehackquest-backend/conf.ini

	name=freehackquest