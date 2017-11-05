# backend-tests

##Set the settings

Create test database by sql-queries:

	> CREATE DATABASE `test` CHARACTER SET utf8 COLLATE utf8_general_ci;
	> GRANT ALL PRIVILEGES ON test.* TO 'freehackquest_u'@'localhost' WITH GRANT OPTION;
	> FLUSH PRIVILEGES;

Change /etc/freehackquest-backend/conf.ini
	name=test

##Requirements

Install pytest

	$ sudo apt install python-pip
	$ pip3 install -U pytest

##Run tests

Check work freehackquestbackend and mysql 
Download repo and change directory to repo
	$ git clone https://github.com/freehackquest/backend-tests.git
	$ cd ./backend-tests
	$ pytest