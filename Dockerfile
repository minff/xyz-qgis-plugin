FROM qgis/qgis:final-3_4_4
# FROM qgis/qgis:final-3_2_2

# https://github.com/travis-ci/docker-sinatra/blob/master/Dockerfile
# https://github.com/hunter-packages/travis-linux-docker/blob/master/Dockerfile

MAINTAINER minff <https://github.com/minff>

RUN mkdir /xyz_qgis_plugin
COPY . /xyz_qgis_plugin
RUN ls /xyz_qgis_plugin
RUN ls /usr/share/qgis
RUN ls /usr/bin/qgis
RUN ls /usr/lib/qgis
RUN which python
RUN which python3
# /usr/lib/python3/dist-packages/qgis

RUN cd /xyz_qgis_plugin && echo alias python_qgis="python3" > env.sh && cat env.sh

RUN find / -name "qgis"