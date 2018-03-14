#!/bin/bash
cd /opt/superdesk/client/dist &&
sed -i -e "s/http:\/\/localhost:5000\/api/$(echo $SUPERDESK_URL | sed 's/\//\\\//g')/g" app*.js -e "s/ws:\/\/localhost:5100/$(echo $SUPERDESK_WS_URL | sed 's/\//\\\//g')/g" &&
nginx &

cd /opt/superdesk &&
bash ./scripts/fig_wrapper.sh honcho start
