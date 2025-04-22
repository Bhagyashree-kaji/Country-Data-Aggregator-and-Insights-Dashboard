# Deployment Guide

This document describes how to deploy the Country Data Aggregator application using Docker.

## Prerequisites

- Docker and Docker Compose installed
- Git for version control
- Free account on Docker Hub
- Student account for cloud hosting (Oracle Cloud, GCP, or GitHub Student Pack)

## Local Development Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/country-data-aggregator.git
   cd country-data-aggregator
   ```

2. **Set up environment variables**
   Create a .env file with the following variables:
   ```
   PGUSER=postgres
   PGPASSWORD=your_password
   PGDATABASE=countrydata
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   Open http://localhost:5000 in your browser

## Production Deployment

### Option 1: Deploying to Oracle Cloud Free Tier

1. **Sign up for Oracle Cloud Free Tier**
   - Go to [oracle.com/cloud/free](https://www.oracle.com/cloud/free/)
   - Register for the Always Free tier with your student email

2. **Create a VM instance**
   - Navigate to Compute > Instances > Create Instance
   - Choose an Always Free eligible shape (VM.Standard.E2.1.Micro)
   - Set up SSH access and note your public IP

3. **Connect to your instance**
   ```bash
   ssh -i /path/to/private_key opc@your_instance_ip
   ```

4. **Install Docker and Docker Compose**
   ```bash
   sudo yum update -y
   sudo yum install -y docker
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo usermod -aG docker opc
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

5. **Deploy the application**
   ```bash
   # Clone your repository or upload files
   git clone https://github.com/yourusername/country-data-aggregator.git
   cd country-data-aggregator
   
   # Create .env file
   cp .env.example .env
   # Edit with secure passwords
   
   # Start the services
   docker-compose up -d
   ```

6. **Configure firewall rules**
   - Navigate to your VM's Virtual Cloud Network
   - Add an ingress rule for port 5000

### Option 2: Deploying to Google Cloud Platform (with student credits)

1. **Sign up for Google Cloud**
   - Go to [cloud.google.com](https://cloud.google.com/)
   - Apply for student credits through [Google for Education](https://edu.google.com/programs/students/)

2. **Install Google Cloud SDK**
   - Download from [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
   - Initialize with `gcloud init`

3. **Set up Docker configuration for Google Cloud**
   ```bash
   # Configure Docker to use gcloud as a credential helper
   gcloud auth configure-docker
   ```

4. **Build and push your Docker image**
   ```bash
   # Tag your image for Google Container Registry
   docker build -t gcr.io/your-project-id/country-data-aggregator:latest .
   
   # Push to Google Container Registry
   docker push gcr.io/your-project-id/country-data-aggregator:latest
   ```

5. **Set up Cloud SQL (PostgreSQL)**
   - Navigate to SQL in the GCP console
   - Create a new PostgreSQL instance (choose the smallest tier)
   - Create a database named `countrydata`
   - Note the connection details

6. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy country-data-aggregator \
     --image gcr.io/your-project-id/country-data-aggregator:latest \
     --platform managed \
     --allow-unauthenticated \
     --set-env-vars="DATABASE_URL=postgresql://username:password@/countrydata?host=/cloudsql/INSTANCE_CONNECTION_NAME"
   ```

### Option 3: Deploying with GitHub Student Pack and DigitalOcean

1. **Sign up for GitHub Student Pack**
   - Go to [education.github.com/pack](https://education.github.com/pack)
   - Register with your student email

2. **Redeem DigitalOcean credits**
   - Follow the link in GitHub Student Pack to redeem DigitalOcean credits
   - Create a new account or link an existing one

3. **Create a Droplet**
   - Choose Marketplace > Docker
   - Select the $5/month plan (smallest)
   - Choose a datacenter region close to your users
   - Add your SSH key or set up a password

4. **Connect to your Droplet**
   ```bash
   ssh root@your_droplet_ip
   ```

5. **Deploy the application**
   ```bash
   # Clone your repository
   git clone https://github.com/yourusername/country-data-aggregator.git
   cd country-data-aggregator
   
   # Create .env file
   cp .env.example .env
   # Edit with secure passwords
   
   # Start the services
   docker-compose up -d
   ```

## Continuous Deployment

For automated deployments:

1. **Set up GitHub Actions**
   Create `.github/workflows/deploy.yml`:
   ```yaml
   name: Deploy

   on:
     push:
       branches: [ main ]

   jobs:
     build-and-push:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Login to Docker Hub
           uses: docker/login-action@v2
           with:
             username: ${{ secrets.DOCKER_HUB_USERNAME }}
             password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
         
         - name: Build and push
           uses: docker/build-push-action@v4
           with:
             push: true
             tags: yourusername/country-data-aggregator:latest
   ```

2. **Configure GitHub repository secrets**
   - Go to your GitHub repository > Settings > Secrets
   - Add `DOCKER_HUB_USERNAME` and `DOCKER_HUB_ACCESS_TOKEN`

3. **Set up webhook-based deployment**
   On your server:
   ```bash
   # Create a script to pull and restart
   cat > /root/deploy.sh << 'EOL'
   #!/bin/bash
   cd /path/to/country-data-aggregator
   git pull
   docker-compose pull
   docker-compose up -d --build
   EOL
   
   chmod +x /root/deploy.sh
   ```

## Troubleshooting

- **Container fails to start**: Check logs with `docker logs container_id`
- **Database connection issues**: Verify environment variables and network connectivity
- **Out of memory errors**: Adjust container resource limits in docker-compose.yml

## Maintenance

- **Updating the application**: 
  ```bash
  # Pull the latest code
  git pull
  
  # Rebuild and restart containers
  docker-compose up -d --build
  ```

- **Database backups**: 
  ```bash
  # Create a backup
  docker exec -t container_id pg_dump -U postgres countrydata > backup.sql
  
  # Restore from backup
  cat backup.sql | docker exec -i container_id psql -U postgres countrydata
  ```

- **Monitoring**: Use free monitoring tools like Prometheus + Grafana, or platform-provided monitoring

## Free Hosting Resources for Students

1. **GitHub Student Pack**: [education.github.com/pack](https://education.github.com/pack)
   - Includes credits for DigitalOcean, Heroku, and other platforms

2. **Oracle Cloud Free Tier**: [oracle.com/cloud/free](https://www.oracle.com/cloud/free/)
   - Always Free resources including compute instances and Autonomous Database

3. **Google Cloud for Students**: [edu.google.com/programs/students](https://edu.google.com/programs/students/)
   - $300 in free credits for GCP services

4. **Azure for Students**: [azure.microsoft.com/free/students](https://azure.microsoft.com/free/students/)
   - $100 in credits and free services for a year

5. **AWS Educate**: [aws.amazon.com/education/awseducate](https://aws.amazon.com/education/awseducate/)
   - AWS credits and free training for students