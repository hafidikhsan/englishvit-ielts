FROM nginx:1.21-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY conf.d/app.conf /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/nginx.conf