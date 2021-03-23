FROM node:stretch-slim
RUN npm install -g serve
COPY . /app
WORKDIR /app
ENTRYPOINT ["serve -s build"]
