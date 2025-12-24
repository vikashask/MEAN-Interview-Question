# Deployment

## Docker

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

CMD ["node", "index.js"]
```

```bash
# Build image
docker build -t my-app:1.0.0 .

# Run container
docker run -p 3000:3000 -e NODE_ENV=production my-app:1.0.0

# Push to registry
docker tag my-app:1.0.0 myregistry/my-app:1.0.0
docker push myregistry/my-app:1.0.0
```

## Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      NODE_ENV: production
      DATABASE_URL: mongodb://mongo:27017/mydb
    depends_on:
      - mongo
    restart: unless-stopped

  mongo:
    image: mongo:5
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    restart: unless-stopped

volumes:
  mongo-data:
```

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app
```

## Heroku Deployment

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create my-app

# Set environment variables
heroku config:set NODE_ENV=production
heroku config:set JWT_SECRET=your-secret

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Scale dynos
heroku ps:scale web=2
```

## AWS Deployment

```bash
# Deploy to Elastic Beanstalk
eb init -p node.js-18 my-app
eb create my-app-env
eb deploy

# Deploy to EC2
# 1. Launch EC2 instance
# 2. SSH into instance
# 3. Install Node.js and npm
# 4. Clone repository
# 5. Install dependencies
# 6. Start application with PM2

npm install -g pm2
pm2 start index.js --name "my-app"
pm2 startup
pm2 save
```

## PM2 Process Manager

```bash
# Install PM2
npm install -g pm2

# Start application
pm2 start index.js --name "my-app"

# Start with cluster mode
pm2 start index.js -i max --name "my-app"

# Monitor
pm2 monit

# View logs
pm2 logs my-app

# Restart
pm2 restart my-app

# Stop
pm2 stop my-app

# Delete
pm2 delete my-app

# Save process list
pm2 save

# Resurrect on reboot
pm2 startup
```

```javascript
// ecosystem.config.js
module.exports = {
  apps: [
    {
      name: "my-app",
      script: "./index.js",
      instances: "max",
      exec_mode: "cluster",
      env: {
        NODE_ENV: "production",
        PORT: 3000,
      },
      error_file: "./logs/error.log",
      out_file: "./logs/out.log",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
    },
  ],
};
```

## CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
          cache: "npm"

      - run: npm ci
      - run: npm test
      - run: npm run lint

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: my-app
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

## Environment Management

```bash
# .env.production
NODE_ENV=production
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/db
JWT_SECRET=your-secret-key
API_KEY=your-api-key
LOG_LEVEL=info

# .env.development
NODE_ENV=development
DATABASE_URL=mongodb://localhost:27017/mydb
JWT_SECRET=dev-secret
LOG_LEVEL=debug
```

```javascript
// config.js
require("dotenv").config();

module.exports = {
  nodeEnv: process.env.NODE_ENV || "development",
  port: process.env.PORT || 3000,
  databaseUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
  apiKey: process.env.API_KEY,
  logLevel: process.env.LOG_LEVEL || "info",
};
```

## Reverse Proxy with Nginx

```nginx
# /etc/nginx/sites-available/my-app
upstream app {
  server localhost:3000;
  server localhost:3001;
  server localhost:3002;
}

server {
  listen 80;
  server_name example.com;

  # Redirect to HTTPS
  return 301 https://$server_name$request_uri;
}

server {
  listen 443 ssl http2;
  server_name example.com;

  ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

  # Gzip compression
  gzip on;
  gzip_types text/plain text/css application/json application/javascript;

  # Cache static files
  location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }

  # Proxy to Node.js
  location / {
    proxy_pass http://app;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cache_bypass $http_upgrade;
  }
}
```

## Health Checks & Auto-restart

```javascript
// graceful-shutdown.js
const gracefulShutdown = async (signal) => {
  console.log(`${signal} received, shutting down gracefully`);

  // Stop accepting new requests
  server.close(async () => {
    // Close database connections
    await mongoose.connection.close();

    // Close Redis connections
    await redis.quit();

    console.log("Server closed");
    process.exit(0);
  });

  // Force shutdown after timeout
  setTimeout(() => {
    console.error("Forced shutdown");
    process.exit(1);
  }, 30000);
};

process.on("SIGTERM", () => gracefulShutdown("SIGTERM"));
process.on("SIGINT", () => gracefulShutdown("SIGINT"));
```
