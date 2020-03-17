# IAM policy to give the origin access identity access to the project bucket
data "aws_iam_policy_document" "project_bucket_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.project_bucket.arn}/*"]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.origin_access_identity.iam_arn]
    }
  }
}

# IAM role for CodeBuild
resource "aws_iam_role" "codebuild_role" {
  name = "${var.project_name}-codebuild-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "codebuild.amazonaws.com",
          "codepipeline.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# Policy to attach to CodeBuild IAM role
resource "aws_iam_policy" "codebuild_policy" {
  name = "${var.project_name}-codebuild-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "codebuild:*",
      "Resource": [
        "${aws_codebuild_project.stage_frontend_codebuild.id}",
        "${aws_codebuild_project.stage_backend_codebuild.id}",
        "${aws_codebuild_project.prod_frontend_codebuild.id}",
        "${aws_codebuild_project.prod_backend_codebuild.id}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters"
      ],
      "Resource": [
        "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/stage/${var.project_name}/*",
        "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:parameter/prod/${var.project_name}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "${aws_s3_bucket.project_bucket.arn}",
        "${aws_s3_bucket.project_bucket.arn}/*"
      ]  
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:*",
        "cloudformation:*",
        "cloudfront:*",
        "iam:*",
        "lambda:*",
        "apigateway:*",
        "route53:*",
        "acm:*"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "codebuild_policy_attachment" {
  name       = "${var.project_name}-codebuild-policy-attachment"
  policy_arn = aws_iam_policy.codebuild_policy.arn
  roles      = [aws_iam_role.codebuild_role.id]
}
