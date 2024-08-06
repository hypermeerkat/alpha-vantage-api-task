# Alpha Vantage Task - Daily Average API

## Project Overview

This project is a full-stack application that provides a daily average API for various commodities using the Alpha Vantage API. It consists of a Flask backend and a React frontend, both containerized and deployed to Azure Web Apps.

The frontend of the application is publicly accessible at [https://alpha-vantage-task-frontend.azurewebsites.net/](https://alpha-vantage-task-frontend.azurewebsites.net/).

### Components

1. **Backend (Flask)**
   - Located in `alpha-vantage-task-backend/`
   - Provides an API endpoint `/daily_average` that fetches data from Alpha Vantage and calculates the daily average price for a given commodity and date range.
   - Implements caching to reduce API calls to Alpha Vantage.
   - Handles error cases and provides appropriate responses.

2. **Frontend (React)**
   - Located in `alpha-vantage-task-frontend/`
   - Provides a user interface for interacting with the backend API.
   - Allows users to select a commodity, date range, and interval.
   - Displays the calculated average price and other relevant information.

3. **Infrastructure (Terraform)**
   - Located in `terraform/`
   - Defines the Azure infrastructure required to host the application.
   - Sets up Azure Web Apps for both frontend and backend.
   - Configures Azure Container Registry for storing Docker images.

4. **CI/CD (GitHub Actions)**
   - Defined in `.github/workflows/main.yaml`
   - Automates the testing, building, and deployment process.
   - Builds Docker images for both frontend and backend.
   - Pushes images to Azure Container Registry.
   - Deploys the latest images to Azure Web Apps.

## Local Development

### Prerequisites

- Python 3.9
- Node.js and npm
- Docker and Docker Compose
- Azure CLI
- Terraform

### Setting up the Backend

1. Navigate to the backend directory:
   ```
   cd alpha-vantage-task-backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Alpha Vantage API key:
   ```
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   ```

5. Run the Flask application:
   ```
   flask run
   ```

### Setting up the Frontend

1. Navigate to the frontend directory:
   ```
   cd alpha-vantage-task-frontend
   ```

2. Install the required packages:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. Note that some the environment configurations will need to be changes when developing locally. For example, the `REACT_APP_API_URL` environment variable will need to be set to `http://localhost:5000` when developing locally. The preferred method is to use a .env file to store these variables. If possible development should be done in a containerised environment and deployed to Azure using the CI/CD pipeline.


### Running with Docker Compose

You can also run both the frontend and backend using Docker Compose:

1. Make sure you have Docker and Docker Compose installed.

2. From the root directory of the project, run:
   ```
   docker-compose up --build
   ```

This will build and start both the frontend and backend containers.

## Pushing Changes and Deploying

1. Make your changes to the codebase.

2. Commit your changes:
   ```
   git add .
   git commit -m "Description of your changes"
   ```

3. Push your changes to the main branch:
   ```
   git push origin main
   ```

4. The GitHub Actions workflow will automatically trigger when changes are pushed or merged into the main branch. Best practice is to create a new branch for each feature or bug fix snd then raise a PR to merge the changes into the main branch. You can monitor its progress in the "Actions" tab of your GitHub repository.

5. Once the workflow completes successfully, your changes will be deployed to the Azure Web Apps.

## Infrastructure Management

To make changes to the infrastructure:

1. Navigate to the `terraform` directory.

2. Make your changes to the Terraform files.

3. Initialize Terraform (if not done before):
   ```
   terraform init
   ```

4. Plan your changes:
   ```
   terraform plan
   ```

5. Apply the changes:
   ```
   terraform apply
   ```

## Testing

- Backend tests are located in `alpha-vantage-task-backend/test_app.py`
- Frontend tests are located in `alpha-vantage-task-frontend/src/App.test.js`

To run backend tests:
```
cd alpha-vantage-task-backend
pytest
```

To run frontend tests:
```
cd alpha-vantage-task-frontend
npm test
```


## Production Environment Improvements

For a robust production deployment, the following improvements should be considered:

### Performance and Scalability
1. **Redis Caching**: Implement Redis for efficient caching of API responses, reducing load on the Alpha Vantage API and improving response times.
2. **Load Balancing**: Utilize Azure Load Balancer or Application Gateway to distribute traffic across multiple instances of the application.
3. **Auto-scaling**: Configure auto-scaling rules in Azure to handle varying loads efficiently.

### Environment Management
1. **Staging Environment**: Set up a separate staging environment for testing before production deployment.
2. **Environment-specific Configurations**: Use environment variables or Azure App Configuration to manage different settings for staging and production.

### Deployment and Infrastructure
1. **Terraform Deployment Tool**: Utilize a tool like Spacelift for managing Terraform deployments, providing better collaboration and audit trails.
2. **Blue-Green Deployments**: Implement blue-green deployment strategy for zero-downtime updates.
3. **Containerization Improvements**: Optimize Docker images for production, including multi-stage builds and security scanning.

### Monitoring and Logging
1. **Application Insights**: Integrate Azure Application Insights for detailed performance monitoring and diagnostics.
2. **Centralized Logging**: Implement ELK stack (Elasticsearch, Logstash, Kibana) or use Azure Log Analytics for centralized log management.
3. **External Monitoring**: Integrate tools like Datadog for comprehensive monitoring and alerting.
4. **Metrics and Visualization**: Set up Grafana and Prometheus for advanced metric gathering and data visualization.

### Security Enhancements
1. **Web Application Firewall (WAF)**: Implement Azure WAF to protect against common web vulnerabilities.
2. **Network Security Groups (NSGs)**: Configure NSGs to control inbound and outbound traffic.
3. **Azure Security Center**: Enable and utilize Azure Security Center for security recommendations and threat protection.
4. **Automated Bot Detection**: Implement bot detection and prevention mechanisms, possibly using Azure Bot Service or third-party solutions.
5. **Regular Security Audits**: Schedule and perform regular security audits and penetration testing.

### Compliance and Governance
1. **GDPR Compliance**: Ensure data handling practices comply with GDPR and other relevant regulations.
2. **Access Control**: Implement Azure AD for robust identity and access management.
3. **Encryption**: Enable encryption at rest and in transit for all sensitive data.

### Backup and Disaster Recovery
1. **Automated Backups**: Set up regular automated backups of databases and critical data.
2. **Disaster Recovery Plan**: Develop and test a comprehensive disaster recovery plan.
3. **Multi-region Deployment**: Consider deploying the application across multiple Azure regions for high availability.

### Performance Optimization
1. **CDN Integration**: Use Azure CDN to serve static content and reduce latency for global users.
2. **Database Optimization**: Implement database indexing and query optimization for improved performance.

### API Management
1. **Azure API Management**: Utilize Azure API Management for better control, documentation, and monetization of APIs.

### Continuous Improvement
1. **User Feedback Loop**: Implement mechanisms to gather and analyze user feedback for continuous improvement.
2. **A/B Testing**: Set up infrastructure for A/B testing of new features.

Implementing these improvements will significantly enhance the reliability, performance, and security of the application in a production environment.