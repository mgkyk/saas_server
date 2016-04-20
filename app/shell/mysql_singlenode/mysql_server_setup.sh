#!/bin/bash
#
# author: ChuXiaokai
# date: 2016/3/30

## create group and user
useradd -s /sbin/nologin -M mysql
## priviledge
chown -R root.mysql /usr/local/mysql
chown -R mysql.mysql /usr/local/mysql/data
bash scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql
/usr/local/mysql/scripts/mysql_install_db --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data --user=mysql
cp support-files/my-medium.cnf /etc/my.cnf
cp support-files/mysql.server /etc/init.d/mysqld
chmod +x /etc/init.d/mysqld

## revise
sed -i '$a [mysqld]\nuser=mysql\ncharacter_set_server=utf8\ndatadir=/usr/local/mysql/data\nbasedir=/usr/local/mysql' /etc/my.cnf

/etc/init.d/mysqld start
echo "mysql start"
