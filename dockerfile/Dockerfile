FROM centos:6

ENV APPS_DIR=/opt/apps
ENV PYTHON_ENV=myenv

RUN yum -y install git-core vim   &&\
    yum clean all

RUN curl -sSL https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh \
         -o /tmp/miniconda.sh                                                     &&\
    bash /tmp/miniconda.sh -bfp /usr/local                                        &&\
    rm -rf /tmp/miniconda.sh                                                      &&\
    conda update conda                                                            &&\
    conda clean --all --yes                                                       &&\
    conda config --add channels conda-forge                                       &&\
    conda config --set always_yes yes --set changeps1 no                          &&\
    conda create -n $PYTHON_ENV python=2.7                                        &&\
    source activate $PYTHON_ENV

RUN source activate $PYTHON_ENV                                   &&\
    conda install flask                                           &&\
    conda install gunicorn                                        &&\
    conda install gevent                                          &&\
    conda install pytest                                          &&\
    conda install celery                                          &&\
    conda clean --all --yes                                       &&\
    pip install flask-restful                                     &&\
    pip install flask-cors

RUN source activate $PYTHON_ENV                                                 &&\
    git clone https://github.com/brendancol/nginx-gunicorn-flask.git $APPS_DIR  &&\
    cd $APPS_DIR                                                                &&\
    pip install -e .

RUN source activate $PYTHON_ENV                                      &&\
    pip install supervisor                                           &&\
    mkdir -p /etc/supervisor                                         &&\
    cp $APPS_DIR/devops/supervisord.conf /etc/supervisor/            &&\
    cp $APPS_DIR/devops/gunicorn_supervisor.ini /etc/supervisor/     &&\
    cp $APPS_DIR/devops/supervisord.sh /etc/rc.d/init.d/supervisord  &&\
    chmod +x /etc/rc.d/init.d/supervisord                            &&\
    chkconfig --add supervisord

RUN rpm -U --quiet http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm &&\
    yum -y install nginx                                  &&\
    mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf-orig   &&\
    cp $APPS_DIR/devops/nginx.conf /etc/nginx/            &&\
    yum clean all

RUN source activate $PYTHON_ENV     && \
    conda install psutil


EXPOSE 80
EXPOSE 8000
EXPOSE 8080

COPY bin/init.sh /init.sh

CMD ["/bin/bash", "--rcfile", "/init.sh"]
