FROM node:alpine

ENV NODE_ENV=production

WORKDIR /app

COPY ["package.json", "package-lock.json*", "./"]

RUN npm install

RUN mkdir /app/.npm-global
RUN npm config set prefix "/app/.npm-global"
ENV PATH="/app/.npm-global/bin:${PATH}"

USER node
COPY . .

# RUN chown -R 1000140000:0 /.npm

CMD ["npm", "start"]