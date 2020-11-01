FROM node:14.15-alpine as builder
WORKDIR /opt/order-ui

COPY ./public/ /opt/order-ui/public/
COPY ./src/ /opt/order-ui/src/
COPY ./package.json /opt/order-ui/package.json
COPY ./package-lock.json /opt/order-ui/package-lock.json
COPY ./babel.config.js /opt/order-ui/babel.config.js
COPY ./tsconfig.json /opt/order-ui/tsconfig.json
COPY ./.browserslistrc /opt/order-ui/.browserslistrc
COPY ./.eslintrc.js /opt/order-ui/.eslintrc.js

ARG VUE_APP_APIHOST="https://api.example.com"
ARG VUE_APP_APITOKEN="dummy"

RUN npm install && npm run build

FROM nginx:1.19-alpine as production
WORKDIR /usr/share/nginx/html
COPY --from=builder /opt/order-ui/dist/ /usr/share/nginx/html/
EXPOSE 80
