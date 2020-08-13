FROM node:13.12.0-alpine
RUN npm install -g create-react-app

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_PATH=/app/src

COPY package.json ./
COPY package-lock.json ./
RUN npm install

COPY . /app

EXPOSE 3000
