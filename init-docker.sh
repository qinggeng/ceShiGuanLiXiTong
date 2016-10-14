docker rm -f ceShiGuanLiContainer
docker run -d --name ceShiGuanLiContainer -p 8081:8000 -v `realpath site`:/usr/local/src/site python:2.7.12 /bin/bash
