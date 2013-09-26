FROM ubuntu:12.04
MAINTAINER Li Meng Jun "lmjubuntu@gmail.com"

RUN echo 'deb http://mirrors.sohu.com/ubuntu/ precise main' > /etc/apt/sources.list
RUN echo 'deb http://mirrors.sohu.com/ubuntu/ precise universe' >> /etc/apt/sources.list
RUN apt-get update

# Set the env variable DEBIAN_FRONTEND to noninteractive
ENV DEBIAN_FRONTEND noninteractive

# Installing the environment required: ssh
RUN apt-get install -y ssh sudo pwgen

# Set locale (fix the locale warnings)
RUN localedef -v -c -i en_US -f UTF-8 en_US.UTF-8 || :

RUN mkdir -p /var/run/sshd

# Copy the files into the container
ADD . /src

EXPOSE 22
# Start ssh services.
CMD ["/bin/bash", "/src/startup.sh"]
