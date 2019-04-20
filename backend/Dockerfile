FROM alpine:3.9.3
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache nodejs nodejs-npm

RUN npm install -g serverless

COPY package.json package-lock.json ./
RUN npm install

RUN apk add --no-cache build-base python3 python3-dev libffi-dev libressl-dev linux-headers mariadb-connector-c-dev

COPY requirements.txt /
RUN pip3 install -r requirements.txt

ADD ./ /backend
WORKDIR /backend

ENV PATH /node_modules/.bin:$PATH

EXPOSE 5000
