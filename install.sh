# master install file for processing architecture (RHEL)

APPS_DIR=/opt/apps

# install nginx repository
rpm -Uvh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm

# install nginx
yum install nginx

# install supervisor, gunicorn, flask
/home/vagrant/miniconda2/bin/conda install flask -y
/home/vagrant/miniconda2/bin/conda install flask-cors -y
/home/vagrant/miniconda2/bin/conda install supervisor -y
/home/vagrant/miniconda2/bin/conda install gunicorn -y
/home/vagrant/miniconda2/bin/conda install gevent -y

# using pip
/home/vagrant/miniconda2/bin/pip install flask-restful

# copy the conf files to the correct place

sudo service nginx stop
sudo mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf-orig
sudo cp $APPS_DIR/devops/nginx.conf /etc/nginx/

sudo service nginx start

# create supervisor config folder and copy config files to it
sudo pmkdir /etc/supervisor
sudo cp $APPS_DIR/devops/supervisord.conf /etc/supervisor/
sudo cp $APPS_DIR/devops/gunicorn_supervisor.ini /etc/supervisor/

sudo cp $APPS_DIR/devops/supervisord.sh /etc/init.d/
sudo chmod +x /etc/init.d/supervisor.sh
sudo /etc/init.d/supervisor.sh start
sudo chkconfig --add supervisord