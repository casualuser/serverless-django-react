FROM alpine:3.9.3

RUN apk add --no-cache python3
RUN pip3 install awscli

RUN apk add --no-cache nodejs nodejs-npm

COPY package.json package-lock.json ./
RUN npm install

ADD ./ /frontend
WORKDIR /frontend
ENV PATH /node_modules/.bin:$PATH

EXPOSE 3000
