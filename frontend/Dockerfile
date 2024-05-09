FROM node:21

WORKDIR /app

COPY package.json package-lock.json /app/

RUN npm ci

COPY .eslintrc.cjs /app/
COPY index.html /app/
COPY tsconfig.json /app/
COPY tsconfig.node.json /app/
COPY tsconfig.json /app/
COPY vite.config.ts /app/
COPY postcss.config.js /app/
COPY tailwind.config.js /app/

COPY public /app/public
COPY src /app/src

EXPOSE 5173

ENTRYPOINT ["npm", "run", "docker-dev"]
