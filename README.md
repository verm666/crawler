Setup, test and run in developer mode
=====================================

* setup

```shell
sudo apt-get install python-dev python-virtualenv build-essential

git clone https://github.com/verm666/crawler
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

Using "git clone" and so on in production - not a better way. For production you should
build deb packages. For building deb package from python project I use my own CDBS helper:
https://gist.github.com/verm666/865e3d8849f49a152559

* setup

```shell
apt-get install crawler
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
