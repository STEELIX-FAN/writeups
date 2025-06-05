FROM ubuntu:22.04@sha256:a6d2b38300ce017add71440577d5b0a90460d0e57fd7aec21dd0d1b0761bbfb2

RUN apt-get update && apt-get install -y xinetd
ENV TERM=linux

RUN useradd -ms /bin/bash ctf

ADD ./share/chall /home/ctf

RUN echo "#!/bin/bash\ntimeout 60 /home/ctf/chall" \
        > /home/ctf/run.sh
RUN chown -R root:ctf /home/ctf
RUN chmod -R 750 /home/ctf

ADD ./babyheap.xinetd /etc/xinetd.d/babyheap
CMD ["/usr/sbin/xinetd", "-dontfork"]
