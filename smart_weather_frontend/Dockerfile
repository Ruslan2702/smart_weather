FROM node:13.12.0-alpine
RUN npm install -g create-react-app

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts@3.4.1 -g

COPY . /app

EXPOSE 3000
