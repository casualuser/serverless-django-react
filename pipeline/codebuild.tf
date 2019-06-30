resource "aws_codebuild_project" "stage_codebuild" {
  name = "${var.name}-stage-codebuild"
  build_timeout = "30"
  service_role = "${aws_iam_role.codebuild_role.arn}"

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image = "aws/codebuild/standard:1.0"
    type = "LINUX_CONTAINER"

    environment_variable {
      "name"  = "REACT_APP_AZURE_APP_ID"
      "value" = "/stage/${var.name}/AZURE_APP_ID"
      "type"  = "PARAMETER_STORE"
    }

    environment_variable {
      "name"  = "REACT_APP_AZURE_AUTHORITY"
      "value" = "/stage/${var.name}/AZURE_AUTHORITY"
      "type"  = "PARAMETER_STORE"
    }

    environment_variable {
      "name"  = "REACT_APP_FRONTEND_URL"
      "value" = "https://${var.stage_domain}"
    }

    environment_variable {
      "name"  = "REACT_APP_BACKEND_URL"
      "value" = "https://${var.stage_api_domain}"
    }

    environment_variable {
      "name"  = "BACKEND_DOMAIN"
      "value" = "${var.stage_api_domain}"
    }

    environment_variable {
      "name"  = "BACKEND_DOMAIN_CERT_ARN"
      "value" = "${aws_acm_certificate_validation.stage_domain_cert_validation.certificate_arn}"
    }

    environment_variable {
      "name"  = "HOSTED_ZONE_ID"
      "value" = "${aws_route53_zone.stage_hosted_zone.id}"
    }

    environment_variable {
      "name"  = "PROJECT_NAME"
      "value" = "${var.name}"
    }

    environment_variable {
      "name"  = "PROJECT_BUCKET"
      "value" = "${var.project_bucket}"
    }

    environment_variable {
      "name"  = "CLOUDFRONT_DISTRO"
      "value" = "${aws_cloudfront_distribution.stage_distribution.id}"
    }

    environment_variable {
      "name"  = "STAGE"
      "value" = "stage"
    }
  }

  source {
    type = "CODEPIPELINE"
    buildspec = "pipeline/buildspec.yml"
  }

  artifacts {
    type = "CODEPIPELINE"
  }
}

resource "aws_codebuild_project" "prod_codebuild" {
  name = "${var.name}-prod-codebuild"
  build_timeout = "30"
  service_role = "${aws_iam_role.codebuild_role.arn}"

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image = "aws/codebuild/standard:1.0"
    type = "LINUX_CONTAINER"

    environment_variable {
      "name"  = "REACT_APP_AZURE_APP_ID"
      "value" = "/prod/${var.name}/AZURE_APP_ID"
      "type"  = "PARAMETER_STORE"
    }

    environment_variable {
      "name"  = "REACT_APP_AZURE_AUTHORITY"
      "value" = "/prod/${var.name}/AZURE_AUTHORITY"
      "type"  = "PARAMETER_STORE"
    }

    environment_variable {
      "name"  = "REACT_APP_FRONTEND_URL"
      "value" = "https://${var.prod_domain}"
    }

    environment_variable {
      "name"  = "REACT_APP_BACKEND_URL"
      "value" = "https://${var.prod_api_domain}"
    }

    environment_variable {
      "name"  = "BACKEND_DOMAIN"
      "value" = "${var.prod_api_domain}"
    }

    environment_variable {
      "name"  = "BACKEND_DOMAIN_CERT_ARN"
      "value" = "${aws_acm_certificate_validation.prod_domain_cert_validation.certificate_arn}"
    }

    environment_variable {
      "name"  = "HOSTED_ZONE_ID"
      "value" = "${aws_route53_zone.prod_hosted_zone.id}"
    }

    environment_variable {
      "name"  = "PROJECT_NAME"
      "value" = "${var.name}"
    }

    environment_variable {
      "name"  = "PROJECT_BUCKET"
      "value" = "${var.project_bucket}"
    }

    environment_variable {
      "name"  = "CLOUDFRONT_DISTRO"
      "value" = "${aws_cloudfront_distribution.prod_distribution.id}"
    }

    environment_variable {
      "name"  = "STAGE"
      "value" = "prod"
    }
  }

  source {
    type = "CODEPIPELINE"
    buildspec = "pipeline/buildspec.yml"
  }

  artifacts {
    type = "CODEPIPELINE"
  }
}
