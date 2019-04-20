FROM lambci/lambda:build-python3.6

RUN curl --silent --location https://rpm.nodesource.com/setup_11.x | bash -
RUN yum -y install nodejs
RUN npm install -g serverless
COPY package.json package-lock.json ./
RUN npm install

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ADD ./ /backend
WORKDIR /backend

ENV PATH /node_modules/.bin:$PATH

EXPOSE 5000
