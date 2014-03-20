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

Python >= 3.3

asyncio <http://code.google.com/p/tulip>

bottle <http://bottlepy.org>

aiobottle <https://github.com/Lupino/aiobottle.git>

lee <https://github.com/Lupino/lee.git> a orm auto create tables on base sqlite3  or mysql

beaker <http://beaker.readthedocs.org/en/latest/>

oursql <https://github.com/LukeCarrier/py3k-oursql.git> if use mysql

docker <http://www.docker.io/>
