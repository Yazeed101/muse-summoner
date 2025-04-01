# Muse Summoner Deployment Guide

This guide provides instructions for deploying the Muse Summoner system to various hosting platforms for permanent access.

## Deployment Options

### 1. GitHub Pages (Static Frontend Only)

For a simple static frontend that connects to a separately hosted backend:

1. Create a production build of the frontend:
```bash
cd /path/to/muse-summoner
python build_static_frontend.py
```

2. Push the built files to a GitHub repository's `gh-pages` branch:
```bash
cd build
git init
git add .
git commit -m "Deploy to GitHub Pages"
git remote add origin https://github.com/yourusername/muse-summoner.git
git push -f origin master:gh-pages
```

3. Your site will be available at `https://yourusername.github.io/muse-summoner`

### 2. Heroku Deployment

For a full-stack deployment including the backend:

1. Create a `Procfile` in the project root:
```
web: gunicorn app:app
```

2. Create a `runtime.txt` file:
```
python-3.10.12
```

3. Install the Heroku CLI and login:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

4. Create a new Heroku app:
```bash
heroku create muse-summoner
```

5. Push to Heroku:
```bash
git push heroku master
```

6. Your app will be available at `https://muse-summoner.herokuapp.com`

### 3. AWS Elastic Beanstalk

For a scalable cloud deployment:

1. Install the AWS CLI and EB CLI:
```bash
pip install awscli awsebcli
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Initialize EB application:
```bash
eb init -p python-3.10 muse-summoner
```

4. Create an environment:
```bash
eb create muse-summoner-env
```

5. Deploy the application:
```bash
eb deploy
```

6. Your app will be available at the provided EB URL

### 4. Docker Deployment

For containerized deployment:

1. Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

2. Build the Docker image:
```bash
docker build -t muse-summoner .
```

3. Run the container:
```bash
docker run -p 5000:5000 muse-summoner
```

4. For cloud deployment, push to Docker Hub:
```bash
docker tag muse-summoner yourusername/muse-summoner
docker push yourusername/muse-summoner
```

### 5. DigitalOcean App Platform

For a simple managed deployment:

1. Create a `app.yaml` file:
```yaml
name: muse-summoner
services:
- name: web
  github:
    repo: yourusername/muse-summoner
    branch: main
  build_command: pip install -r requirements.txt
  run_command: gunicorn app:app
  http_port: 5000
```

2. Deploy using the DigitalOcean CLI:
```bash
doctl apps create --spec app.yaml
```

## Permanent Access Considerations

### Domain Configuration

For a custom domain:

1. Purchase a domain from a registrar (e.g., Namecheap, GoDaddy)
2. Configure DNS settings to point to your deployment
3. Set up HTTPS with Let's Encrypt or your hosting provider's SSL

### Backup and Restore

To ensure data persistence:

1. Set up regular backups of the memory directory
2. Export configuration and muse profiles regularly
3. Store backups in a secure location (e.g., AWS S3, Google Drive)

### Monitoring and Maintenance

For long-term reliability:

1. Set up monitoring with tools like New Relic or Datadog
2. Configure alerts for downtime or errors
3. Implement logging for troubleshooting
4. Schedule regular updates and maintenance

## GitHub Repository Access

The complete Muse Summoner system is available in the GitHub repository:

```
https://github.com/yourusername/muse-summoner
```

To clone and run locally:

```bash
git clone https://github.com/yourusername/muse-summoner.git
cd muse-summoner
pip install -r requirements.txt
python app.py
```

## Remote Administration

Once deployed, you can administer the system remotely using the Admin API:

1. Obtain an API key:
```bash
curl -X POST https://your-deployment-url.com/api/admin/auth \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

2. Use the API key for remote administration:
```bash
curl -X GET https://your-deployment-url.com/api/admin/config \
  -H "Authorization: Bearer your_api_key"
```

See the DOCUMENTATION.md file for complete API reference.
