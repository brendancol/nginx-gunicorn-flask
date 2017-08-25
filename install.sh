# master install file for processing architecture (RHEL)


wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
chmod a+x Miniconda2-latest-Linux-x86_64.sh
./Minicocurl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.shnda2-latest-Linux-x86_64.sh

curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh
bash /tmp/miniconda.sh -bfp /usr/local
rm -rf /tmp/miniconda.sh

RUN mkdir -p /opt/$NAME
COPY environment-ubuntu.yml /opt/$NAME/environment.yml
ENV PATH /usr/local/envs/gfw-api/bin:$PATH

RUN groupadd $USER && useradd -g $USER $USER -s /bin/bash
RUN conda update conda
RUN conda config --add channels conda-forge 
RUN conda config --set always_yes yes --set changeps1 no
RUN cd /opt/$NAME && conda env create -f environment.yml

COPY entrypoint.sh /opt/$NAME/entrypoint.sh
COPY main.py /opt/$NAME/main.py
COPY gunicorn.py /opt/$NAME/gunicorn.py

