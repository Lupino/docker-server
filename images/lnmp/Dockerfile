FROM ubuntu:12.04
MAINTAINER Li Meng Jun "lmjubuntu@gmail.com"

RUN echo 'deb http://mirrors.sohu.com/ubuntu/ precise main' > /etc/apt/sources.list
RUN echo 'deb http://mirrors.sohu.com/ubuntu/ precise universe' >> /etc/apt/sources.list
RUN apt-get update

# Set the env variable DEBIAN_FRONTEND to noninteractive
ENV DEBIAN_FRONTEND noninteractive

# Installing the environment required: ssh
RUN apt-get install -y ssh sudo pwgen nginx-light vim mysql-server
RUN apt-get install -y php5-fpm php5-gd php5-imap php5-mcrypt php5-mysql
RUN apt-get clean
# Set locale (fix the locale warnings)
RUN localedef -v -c -i en_US -f UTF-8 en_US.UTF-8 || :

RUN mkdir -p /var/run/sshd

# Copy the files into the container
ADD startup.sh /usr/local/bin/run
RUN chmod +x /usr/local/bin/run

EXPOSE 22
EXPOSE 80
# Start ssh services.
CMD ["/usr/local/bin/run"]
