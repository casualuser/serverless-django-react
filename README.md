# serverless-django-react

- Boilerplate code to launch an application with a React frontend and Django backend using serverless architecture
- Pulls parameters from AWS Parameter Store instead of using env files
- Uses Terraform to create deployment pipeline


# First time migration
## Local
  1. `docker-compose exec backend sh`
  2. `sls wsgi manage local -c "migrate"`
