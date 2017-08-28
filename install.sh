# master install file for processing architecture (RHEL)
APPS_DIR=/opt/apps
PYTHON_ENV=myenv
PATH=/usr/local/envs/$PYTHON_ENV/bin:/usr/local/bin:$PATH


# install conda
curl -sSL https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -o /tmp/miniconda.sh
bash /tmp/miniconda.sh -bfp /usr/local
rm -rf /tmp/miniconda.sh
conda clean --all --yes
conda update conda
conda config --add channels conda-forge 
conda config --set always_yes yes --set changeps1 no


# install supervisor, gunicorn, flask
conda create -n $PYTHON_ENV python=2.7
source activate $PYTHON_ENV
conda install flask -y
conda install gunicorn -y
conda install gevent -y
conda install pytest -y
pip install flask-restful
pip install flask-cors
cd $APPS_DIR && python setup.py install


# create supervisor config folder and copy config files to it
pip install supervisor
sudo mkdir -p /etc/supervisor
sudo cp $APPS_DIR/devops/supervisord.conf /etc/supervisor/
sudo cp $APPS_DIR/devops/gunicorn_supervisor.ini /etc/supervisor/
sudo cp $APPS_DIR/devops/supervisord.sh /etc/rc.d/init.d/supervisord
sudo chmod +x /etc/rc.d/init.d/supervisord
sudo service supervisord start
sudo chkconfig --add supervisord


# install nginx
sudo rpm -U --quiet http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
sudo yum -y install nginx
sudo service nginx stop
sudo mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf-orig
sudo cp $APPS_DIR/devops/nginx.conf /etc/nginx/
sudo service nginx start
