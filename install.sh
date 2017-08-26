# master install file for processing architecture (RHEL)

APPS_DIR=/opt/apps

# install nginx repository
rpm -Uvh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm

# install nginx
yum install nginx

# install supervisor, gunicorn
conda install supervisor -y
conda install gunicorn -y

# copy the conf files to the correct place

service nginx stop
mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf-orig
cp $APPS_DIR/devops/nginx.conf /etc/nginx/

service nginx start

# create supervisor config folder and copy config files to it
mkdir /etc/supervisor
cp $APPS_DIR/devops/supervisord.conf /etc/supervisor
cp $APPS_DIR/devops/gunicorn_supervisor.ini