apt-get -qqy update
apt-get -qqy install postgresql
apt-get -qqy install python-psycopg2
apt-get -qqy install python-sqlalchemy
apt-get -qqy install python-flask
apt-get -qqy install python-flask-sqlalchemy
apt-get -qqy install python-pip
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
su postgres -c 'createuser -dRS vagrant'
su postgres -c 'createuser -dRS catalog'
#su vagrant -c 'createdb itemcatalog'

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd

