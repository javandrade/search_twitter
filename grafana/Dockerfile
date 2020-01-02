
FROM grafana/grafana:6.5.0
MAINTAINER Java Andrade <java.andrade@gmail.com>

#RUN apt install update && \
 #   apt install -y curl gettext-base && \
  #  rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh .
#RUN chmod +x entrypoint.sh

####Removendo .init #########################
RUN rm -rf /var/lib/grafana/.init

ENTRYPOINT ["./entrypoint.sh"]
