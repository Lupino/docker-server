This repo provide a easy way for create container use the custem images base
docker, every container has less two export ports.
it use for the private cloud or other.

Usage:
------

    mv config.sample.py config.py
    python3 main.py

Build the base images
---------------------

    cd images/ubuntu-server
    docker build -t lupino/ubuntu .
    # then edit the config.py add the images

Requirements
-----------

Python 3.3

tulip <http://code.google.com/p/tulip>

asynchttp <https://github.com/fafhrd91/asynchttp>

bottle <http://bottlepy.org>

asyncbottle <https://github.com/Lupino/asyncbottle.git>

lee <https://github.com/Lupino/lee.git>

beaker <http://beaker.readthedocs.org/en/latest/>

oursql <https://github.com/LukeCarrier/py3k-oursql.git> if use mysql

docker <http://www.docker.io/>
