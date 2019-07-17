# serverless-django-react

# Description

- Boilerplate code to launch an application with a React frontend and Django backend using serverless architecture
- Pulls parameters from AWS Parameter Store instead of using env files
- Uses Terraform to create deployment pipeline

# Architecture

| Component      | Approach                                           | Notes                                                                                                                                                          |
| -------------- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Frontend       | [React](https://reactjs.org/)                      | - Bootstrapped by [create-react-app](https://github.com/facebook/create-react-app) <br/> - [ANT Design](https://github.com/ant-design/ant-design) UI Framework |
| Backend        | [Django](https://github.com/django/django)         |                                                                                                                                                                |
| Authentication | Azure Active Directory                             | Uses [MSAL](https://github.com/AzureAD/microsoft-authentication-library-for-js) via [react-msal-jwt](https://github.com/stevenphaedonos/react-msal-jwt)        |
| Infrastructure | Serverless (backend), AWS S3/CloudFront (frontend) | [Terraform](https://www.terraform.io/) for infrastructure-as-code, Route53 delegation for DNS, AWS ACM for SSL certificates                                    |
| CI/CD pipeline | AWS + [Terraform](https://www.terraform.io/)       | CodePipeline + GitHub hook + CodeBuild                                                                                                                         |

# Logging/Auditing

- Logs are stored in AWS CloudWatch under path `/serverless/django/<project_name>/<environment/`
- Log streams include:
  - audit
  - MSAL (authentication errors triggered in frontend)
  - watchtower (Django exceptions)

# Configuration

## GitHub Access Token

- [GitHub access token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) stored in AWS Parameter Store in parameter `/GITHUB_TOKEN`
- CodePipeline source configured as a GitHub hook uses this token

## AWS Parameter Store

- Parameters for the project are stored in AWS Parameter Store under path `/<environment>/<project_name>/<parameter>`

| Parameter            | Required | Type         |
| -------------------- | -------- | ------------ |
| AZURE_APP_ID         | Yes      | String       |
| AZURE_AUTHORITY      | Yes      | String       |
| ASSET_URL            | Yes      | String       |
| ASSET_BUCKET         | Yes      | String       |
| AZURE_ADMIN_GROUP_ID | Yes      | String       |
| DB_HOST              | Yes      | String       |
| DB_NAME              | Yes      | String       |
| DB_USER              | Yes      | String       |
| DB_PASSWORD          | Yes      | SecureString |
| DB_PORT              | No       | String       |
| SECRET_KEY           | Yes      | SecureString |
| ALLOWED_HOSTS        | No       | String       |
| CORS_WHITELIST       | No       | String       |

## Terraform

| Parameter             | Required | Description                                                                              |
| --------------------- | -------- | ---------------------------------------------------------------------------------------- |
| project_name          | Yes      | Lower-case project name                                                                  |
| project_bucket        | Yes      | Location to store project files (serverless deployment, compiled frontend, codepipeline) |
| asset_bucket          | Yes      | Location to store project assets (profile pictures)                                      |
| git_repository_owner  | Yes      | Username of the GitHub account which owns the repository                                 |
| git_repository_name   | Yes      | Name of the GitHub code repository                                                       |
| git_repository_branch | Yes      | Name of the branch to pull code from                                                     |
| stage_domain          | Yes      | Used as an environment variable in stage CodeBuild                                       |
| prod_domain           | Yes      | Used as an environment variable in prod CodeBuild                                        |

# Environment parameters

## For development

| Parameter                 | AWS Parameter Store  | Declared in                                                                       | Purpose                                                                                                                                   |
| ------------------------- | -------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| PROJECT_NAME              | N/A                  | [local.env](local.env), [Serverless config](backend/serverless.yml)               | Used in frontend [entrypoint.sh](frontend/entrypoint.sh) to fetch Active Directory configuration, and for backend Serverless service name |
| FRONTEND_URL              | N/A                  | [Docker Compose](docker-compose.yml)                                              | Used if the backend should redirect to the frontend                                                                                       |
| REACT_APP_BACKEND_URL     | N/A                  | [Docker Compose](docker-compose.yml)                                              | Default endpoint configuration for Axios in frontend                                                                                      |
| REACT_APP_FRONTEND_URL    | N/A                  | [Docker Compose](docker-compose.yml)                                              | MSAL configuration in frontend                                                                                                            |
| REACT_APP_AZURE_APP_ID    | AZURE_APP_ID         | [entrypoint.sh](frontend/entrypoint.sh)                                           | MSAL configuration in frontend                                                                                                            |
| REACT_APP_AZURE_AUTHORITY | AZURE_AUTHORITY      | [entrypoint.sh](frontend/entrypoint.sh)                                           | MSAL configuration in frontend                                                                                                            |
| AZURE_APP_ID              | AZURE_APP_ID         | [Serverless config](backend/serverless.yml)                                       | MSAL token decryption/validation in backend                                                                                               |
| AZURE_ADMIN_GROUP_ID      | AZURE_ADMIN_GROUP_ID | [Serverless config](backend/serverless.yml)                                       | Used during authentication process to check if user is in the group and grants administrative privileges in the application               |
| SECRET_KEY                | SECRET_KEY           | [Serverless config](backend/serverless.yml)                                       | Secret key for Django                                                                                                                     |
| DB_HOST                   | N/A                  | [Serverless config](backend/serverless.yml), [Docker Compose](docker-compose.yml) | DB connection settings                                                                                                                    |
| DB_NAME                   | N/A                  | [Serverless config](backend/serverless.yml), [Docker Compose](docker-compose.yml) | DB connection settings                                                                                                                    |
| DB_USER                   | N/A                  | [Serverless config](backend/serverless.yml), [Docker Compose](docker-compose.yml) | DB connection settings                                                                                                                    |
| DB_PASSWORD               | N/A                  | [Serverless config](backend/serverless.yml), [Docker Compose](docker-compose.yml) | DB connection settings                                                                                                                    |  |

## For stage/prod

| Parameter                 | AWS Parameter Store  | Declared in                                 | Purpose                                                                                                                     |
| ------------------------- | -------------------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| STAGE                     | N/A                  | [Serverless config](backend/serverless.yml) | Used in backend to perform functions based on environment/stage                                                             |
| PROJECT_NAME              | N/A                  | [Serverless config](backend/serverless.yml) | Used for backend Serverless service name                                                                                    |
| FRONTEND_URL              | N/A                  | [Serverless config](backend/serverless.yml) | Used if the backend should redirect to the frontend                                                                         |
| REACT_APP_BACKEND_URL     | N/A                  | [CodeBuild](pipeline/codebuild.tf)          | Default endpoint configuration for Axios in frontend                                                                        |
| REACT_APP_FRONTEND_URL    | N/A                  | [CodeBuild](pipeline/codebuild.tf)          | MSAL configuration in frontend                                                                                              |
| REACT_APP_AZURE_APP_ID    | AZURE_APP_ID         | [CodeBuild](pipeline/codebuild.tf)          | MSAL configuration in frontend                                                                                              |
| REACT_APP_AZURE_AUTHORITY | AZURE_AUTHORITY      | [CodeBuild](pipeline/codebuild.tf)          | MSAL configuration in frontend                                                                                              |
| AZURE_APP_ID              | AZURE_APP_ID         | [Serverless config](backend/serverless.yml) | MSAL token decryption/validation in backend                                                                                 |
| AZURE_ADMIN_GROUP_ID      | AZURE_ADMIN_GROUP_ID | [Serverless config](backend/serverless.yml) | Used during authentication process to check if user is in the group and grants administrative privileges in the application |
| SECRET_KEY                | SECRET_KEY           | [Serverless config](backend/serverless.yml) | Secret key for Django                                                                                                       |
| DB_HOST                   | DB_HOST              | [Serverless config](backend/serverless.yml) | DB connection settings                                                                                                      |
| DB_NAME                   | DB_NAME              | [Serverless config](backend/serverless.yml) | DB connection settings                                                                                                      |
| DB_USER                   | DB_USER              | [Serverless config](backend/serverless.yml) | DB connection settings                                                                                                      |
| DB_PASSWORD               | DB_PASSWORD          | [Serverless config](backend/serverless.yml) | DB connection settings                                                                                                      |
| ALLOWED_HOSTS             | ALLOWED_HOSTS        | [Serverless config](backend/serverless.yml) | Django settings for allowing requests from a given origin domain                                                            |
| CORS_WHITELIST            | CORS_WHITELIST       | [Serverless config](backend/serverless.yml) | Django settings for including the given domains in CORS headers of responses                                                |
| TEAMS_WEBHOOK             | TEAMS_WEBHOOK        | [Serverless config](backend/serverless.yml) | Enable message pushes to Teams (e.g. for Django error notifications)                                                        |

# First time migration

## Local

1. `docker-compose exec backend sh`
2. `sh ./init.sh`

# Running the project

1. `docker-compose build`
2. `docker-compose up`
