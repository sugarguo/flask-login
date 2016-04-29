#! /bin/bash

#source ~/.bashrc 

echo "==========================="
echo "please input mode:"
echo "1 mysql do"
echo "2 sqlite do"
echo "3 gunicorn run"
echo "8 clean *.sqlite *~ *.pyc"
echo "9 exit"
echo "==========================="
read input

case $input in
	1)
		echo "mysql do"
		#sleep 1
		echo "please input SECRET_KEY:(long strong)"
		read SECRET_KEY
		echo 'export SECRET_KEY="embedway&sugarguo&blbl"' >> $HOME/.bashrc
		echo '' >> $HOME/.bashrc
		echo "please input mysql url:(Default: 127.0.0.1)"
		read DATABASE_URL
		DATABASE_URL=${DATABASE_URL:-'127.0.0.1'}
		echo $DATABASE_URL
		echo "please input mysql port:(Default: 3306)"
		read DATABASE_PORT
		DATABASE_PORT=${DATABASE_PORT:-'3306'} 
		echo "please input mysql username:(Default: root)"
		read DATABASE_USERNAME
		DATABASE_USERNAME=${DATABASE_USERNAME:-'root'} 
		echo "please input mysql password:(!!Need Input e.g. 123456)"
		read DATABASE_PASSWORD
		if [ ! $DATABASE_PASSWORD ]; then  
		    echo 'not input password sleep2 exit!'
		    sleep 2
		    exit
		fi  
		echo "please input create database:(e.g. db_flask_blog_dev)"
		read DATABASE_DATABASE
		echo 'export DEV_DATABASE_URL="mysql://'$DATABASE_USERNAME':'$DATABASE_PASSWORD'@'$DATABASE_URL':'$DATABASE_PORT'/'$DATABASE_DATABASE'"' >> $HOME/.bashrc
		mysql -u$DATABASE_USERNAME -p$DATABASE_PASSWORD -e"create database "$DATABASE_DATABASE
		echo "please input sql file:(e.g. mysqlfile)"
		read MYSQL_FILE
		mysql -u$DATABASE_USERNAME -p$DATABASE_PASSWORD -e"use "$DATABASE_DATABASE";source "$MYSQL_FILE".sql;"
		echo "all done!  sleep2 exit!"
		sleep 2
		source ~/.bashrc;;
		#python installmysql.py;;
	2)
		echo "sqlite do"
		#echo "please input SECRET_KEY:(long strong)"
		#read SECRET_KEY
		echo 'export SECRET_KEY="embedway&sugarguo&blbl"' >> $HOME/.bashrc
		echo '' >> $HOME/.bashrc
		echo "please input DEV_DATABASE_URL:(e.g. weekly_report_test)"
		read DEV_DATABASE_URL
		echo 'export DEV_DATABASE_URL="sqlite:///'`pwd`'/'$DEV_DATABASE_URL'.sqlite"' >> $HOME/.bashrc
		source ~/.bashrc
		python installsqlite.py;;
	3)
		echo "gunicorn run   gunicorn.conf runserver:app"
		source venv/bin/activate
		gunicorn --config gunicorn.conf runserver:app;;
	8)
		echo "clean *.sqlite *~ *.pyc"
		rm *.sqlite
		find . -name "*~" | xargs rm
		find . -name "*.pyc" | xargs rm;;
	9)
		echo "exit!"
		exit;;
esac

#python manage.py shell

#python runserver.py

#python manage.py runserver -p 2005 -h 0.0.0.1
