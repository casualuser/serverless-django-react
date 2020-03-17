FROM amazonlinux:2.0.20190228

RUN curl --silent --location https://rpm.nodesource.com/setup_11.x | bash -
RUN yum install -y nodejs
COPY package.json package-lock.json ./
RUN npm install

RUN yum install -y awscli

ADD ./ /frontend
WORKDIR /frontend
ENV PATH /node_modules/.bin:$PATH

EXPOSE 3000
