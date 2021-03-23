FROM ubuntu:20.04
RUN apt-get update -y
RUN apt install -y python3 python3-pip
RUN pip3 install flask requests
RUN pip3 install flask-cors
COPY ./api.py /app/api.py
COPY ./functions.py /app/functions.py
COPY ./auth.json /app/auth.json
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["api.py"]
