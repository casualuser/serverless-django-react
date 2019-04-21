# IAM policy to give the origin access identity access to the project bucket
data "aws_iam_policy_document" "project_bucket_policy" {
  statement {
    actions = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.project_bucket.arn}/*"]

    principals {
      type = "AWS"
      identifiers = ["${aws_cloudfront_origin_access_identity.origin_access_identity.iam_arn}"]
    }
  }

  statement {
    actions = ["s3:ListBucket"]
    resources = ["${aws_s3_bucket.project_bucket.arn}"]

    principals {
      type = "AWS"
      identifiers = ["${aws_cloudfront_origin_access_identity.origin_access_identity.iam_arn}"]
    }
  }
}

# IAM role for CodeBuild
resource "aws_iam_role" "codebuild_role" {
  name = "${var.name}-codebuild-role"

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
  name = "${var.name}-codebuild-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "codebuild:*",
      "Resource": [
        "${aws_codebuild_project.stage_codebuild.id}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:GetParameters"
      ],
      "Resource": [
        "arn:aws:ssm:${var.region}:${var.account_id}:parameter/stage/${var.name}/*",
        "arn:aws:ssm:${var.region}:${var.account_id}:parameter/prod/${var.name}/*"
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
        "apigateway:*"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_policy_attachment" "codebuild_policy_attachment" {
  name = "${var.name}-codebuild-policy-attachment"
  policy_arn = "${aws_iam_policy.codebuild_policy.arn}"
  roles = ["${aws_iam_role.codebuild_role.id}"]
}
