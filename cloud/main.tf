provider "aws" {
  region = "us-east-1"
}

# Create ECR Repository
resource "aws_ecr_repository" "fish_backend" {
  name = "fish-backend"
}

# Create IAM Role
resource "aws_iam_role" "app_runner_role" {
  name = "AppRunnerECRAccessRole"

  path = "/service-role/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "build.apprunner.amazonaws.com" }
    }]
  })
}

# Attach the AWS-managed policy for ECR access
resource "aws_iam_role_policy_attachment" "ecr_pull_access" {
  role       = aws_iam_role.app_runner_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# Instance Role for environment variables
resource "aws_iam_role" "instance_role" {
  name = "FishAIInstanceRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "tasks.apprunner.amazonaws.com" }
    }]
  })
}
# Attach the Permission to Read SSM Secrets
resource "aws_iam_role_policy" "ssm_access" {
  name = "FishSSMAccess"
  role = aws_iam_role.instance_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "ssm:GetParameters"
      Resource = "arn:aws:ssm:us-east-1:*:parameter/fish-ai/prod/*"
    }]
  })
}

# Create the App Runner Service
resource "aws_apprunner_service" "fish_service" {
  service_name = "fish-backend-production"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.app_runner_role.arn
    }

    image_repository {
      image_identifier      = "${aws_ecr_repository.fish_backend.repository_url}:latest"
      image_repository_type = "ECR"

      image_configuration {
        port = "5000"

        runtime_environment_secrets = {
          REDIS_URL          = "/fish-ai/prod/REDIS_URL"
          GEMINI_API_KEY     = "/fish-ai/prod/GEMINI_API_KEY"
          ELEVENLABS_API_KEY = "/fish-ai/prod/ELEVENLABS_API_KEY"
        }
      }
    }
  }
  observability_configuration {
    observability_enabled = false
  }

  instance_configuration {
    instance_role_arn = aws_iam_role.instance_role.arn

    cpu    = "512"
    memory = "1024"
  }
}
