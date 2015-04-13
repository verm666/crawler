Setup, test and run in developer mode
=====================================

* setup

```shell
apt-get install python-dev python-virtualenv build-essential

git clone
cd crawler
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

* run tests

```shell
python ./tests/tests.py
```

* run crawler

```shell
./bin/local_run-crawler --help
Usage: local_run-crawler [options]

Options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain=DOMAIN
                        uri for crawling, example: example.com
  -s SCHEME, --scheme=SCHEME
                        available schemas: http and https, [default: https]
  -r REPORT, --report=REPORT
                        path to report.json, [default: /tmp/report.json]
  -p POOL_SIZE, --pool-size=POOL_SIZE
                        eventlet pool size, [default: 100]
  -t TIMEOUT, --timeout=TIMEOUT
                        http request timeout in seconds, [default: 20]


./bin/local_run-crawler --domain=digitalocean.com
```

Setup and run in production mode
================================

* setup

```shell
```

* run

```shell
/usr/bin/crawler --help
Usage: crawler [options]

Options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain=DOMAIN
                        uri for crawling, example: example.com
  -s SCHEME, --scheme=SCHEME
                        available schemas: http and https, [default: https]
  -r REPORT, --report=REPORT
                        path to report.json, [default: /tmp/report.json]
  -p POOL_SIZE, --pool-size=POOL_SIZE
                        eventlet pool size, [default: 100]
  -t TIMEOUT, --timeout=TIMEOUT
                        http request timeout in seconds, [default: 20]


/usr/bin/crawler --domain=digitalocean.com
```
