FROM ubuntu:20.10

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Amsterdam

RUN apt-get update -y 

RUN apt install python3-pip -y
RUN pip install mxnet osmnx flask requests utm scikit-learn

#Expose the required port
EXPOSE 5000

COPY src /routeplanner/src
COPY data /routeplanner/data
COPY config /routeplanner/config

ENTRYPOINT ["python3", "/routeplanner/src/server.py"] 
