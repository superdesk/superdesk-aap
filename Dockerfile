# import base image
FROM ubuntu:trusty

# install system-wide dependencies,
# python3 and the build-time dependencies for c modules
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
build-essential \
curl \
freetds-bin \
freetds-dev \
ftp \
libffi-dev git \
libfontconfig \
libfreetype6-dev \
libjpeg8-dev \
liblcms2-dev \
libtiff5-dev \
libwebp-dev \
libxml2-dev \
libxslt1-dev \
nano \
nginx \
nodejs \
npm \
python3 \
python3-dev \
python3-lxml \
python3-pip \
tdsodbc sqsh \
unixodbc \
unixodbc-dev \
vim \
zlib1g-dev

# misc 
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
rm /etc/nginx/sites-enabled/default && \
ln --symbolic /usr/bin/nodejs /usr/bin/node && \
npm cache clean && \
npm install -g npm && \
npm install -g n && \
n 6.6.0 && \
node -v && \
nodejs -v && \
npm -g install grunt-cli && \
cd /tmp && pip3 install -U pip setuptools && \
locale-gen en_US.UTF-8

# Set the locale
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

# setup the environment
WORKDIR /opt/superdesk/
COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/superdesk_vhost.conf /etc/nginx/sites-enabled/superdesk.conf
COPY ./docker/start.sh /opt/superdesk/start.sh
# copy git revision information (used in "about" screen)
COPY .git/HEAD /opt/superdesk/.git/
COPY .git/refs/ /opt/superdesk/.git/refs/

CMD /opt/superdesk/start.sh

# client ports
EXPOSE   80
EXPOSE  443
EXPOSE 9000
# server ports
EXPOSE 5000
EXPOSE 5100
EXPOSE 5400

# prepare for install of server and client components
ENV PYTHONUNBUFFERED=1 C_FORCE_ROOT="False" CELERYBEAT_SCHEDULE_FILENAME=/tmp/celerybeatschedule.db
COPY ./server/requirements.txt /tmp/requirements.txt
COPY ./server /opt/superdesk
#COPY ./client/package.json /opt/superdesk/client/
COPY ./client /opt/superdesk/client

# install server and client dependencies and sources
RUN cd /tmp && pip3 install -U -r /tmp/requirements.txt && \
cd /opt/superdesk/client && npm install && \
cd /opt/superdesk/client && grunt build --disableEditorToolbar=true --defaultTimezone="Australia/Sydney"

# end of file
