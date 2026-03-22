FROM cypress/included:15.11.0

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npx cypress verify

CMD ["npx", "cypress", "open"]
