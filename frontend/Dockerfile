FROM node:21 as build

WORKDIR /app

ARG VITE_API_HOST
ENV VITE_API_HOST=$VITE_API_HOST

ARG VITE_WITHOUT_AUTH_MODE=false
ENV VITE_WITHOUT_AUTH_MODE=$VITE_WITHOUT_AUTH_MODE

# install dependencies
COPY package.json package-lock.json /app/

RUN npm ci

# copy files
COPY . /app/

FROM build as package

WORKDIR /app

RUN npm run build

FROM nginx:1.25.5 as prod

WORKDIR /app

COPY --from=package /app/dist /app/dist
RUN cp -r /app/dist/* /usr/share/nginx/html
RUN rm -rf /app

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

FROM build as lint

WORKDIR /app

RUN npm run eslint:lint

FROM build as dev

WORKDIR /app

EXPOSE 5173

ENTRYPOINT ["npm", "run", "docker-dev"]
