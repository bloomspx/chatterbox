FROM node:latest

COPY package.json .
RUN npm install && npm cache clean --force 

COPY . .

RUN chown -R 1000140000:0 /root/.npm

CMD ["npm", "start"]