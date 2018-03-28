### Kafka as Message Queue Prototype

### Using separate terminals (or screen / tmux), start the following processes:

##### Setup Python Environment

`conda create -n kafka python=2.7 numpy scikit-image flask`
`source activate kafka`
`pip install kq`


##### Install Kafka / Zookeeper

I did this on OSX using Homebrew

`brew install kafka`

##### Start Prototype

1. Start Zookeeper

```bash
zkserver start
```

2. Start Kafka

```bash
cd /usr/local/Cellar/kafka/1.0.0/bin
./kafka-server-start /usr/local/etc/kafka/server.properties
```

3. Start Worker

```bash
python worker.py
```

4. Start Flask Server

```bash
python app.py
```

##### Usage

1. Open browser (or submit GET request) to `http://localhost:5000/`

2. Visit job endpoint: `http://localhost:5000/abc30213-4329afea-234...`

