FROM qgis/qgis:final-3_4_4
# FROM qgis/qgis:final-3_2_2

# https://github.com/travis-ci/docker-sinatra/blob/master/Dockerfile
# https://github.com/hunter-packages/travis-linux-docker/blob/master/Dockerfile

MAINTAINER minff <https://github.com/minff>

RUN mkdir /xyz_qgis_plugin
COPY . /xyz_qgis_plugin
RUN ls /xyz_qgis_plugin

RUN git clone https://github.com/minff/xyz-qgis-plugin.git /root/xyz_qgis_plugin

# RUN alias python_qgis='"C:/DEV/QGIS 3.4/bin/python-qgis.bat"' 
RUN find . -name "python-qgis"
RUN find . -name "python*"