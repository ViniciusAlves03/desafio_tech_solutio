FROM node:22.22.0-alpine

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install
RUN npm install -g @angular/cli@21.2.0

COPY . .

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0", "--poll", "2000"]
