# import base image
FROM ubuntu:trusty

# Dependencies Kibana misc
RUN apt-get update -qq && apt-get install -y -qq nginx-full wget && mkdir -p /opt/kibana && wget https://download.elastic.co/kibana/kibana/kibana-4.6.4-linux-x86_64.tar.gz -O /tmp/kibana.tar.gz && tar zxf /tmp/kibana.tar.gz && mv kibana-4.6.4-linux-x86_64/* /opt/kibana/ && /opt/kibana/bin/kibana plugin --install elasticsearch/marvel/2.4.4

# Configs
ADD kibana.yml /opt/kibana/config/kibana.yml

EXPOSE 5601

CMD /opt/kibana/bin/kibana
