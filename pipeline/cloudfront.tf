# Origin access identity for CloudFront distros
resource "aws_cloudfront_origin_access_identity" "origin_access_identity" {
  comment = "${var.name}-access-identity"
}


# CloudFront distribution for stage environment
resource "aws_cloudfront_distribution" "stage_distribution" {
  origin {
    domain_name = "${aws_s3_bucket.project_bucket.bucket_domain_name}"
    origin_path = "/stage"
    origin_id = "${aws_s3_bucket.project_bucket.id}"

    s3_origin_config {
      origin_access_identity = "${aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path}"
    }
  }

  enabled = true
  is_ipv6_enabled = true
  default_root_object = "index.html"

  # TODO: aliases & domain cert
  # aliases = ["mysite.example.com", "yoursite.example.com"]

  viewer_certificate {
    cloudfront_default_certificate = true
  }
  default_cache_behavior {
    allowed_methods = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods = ["GET", "HEAD"]
    target_origin_id = "${aws_s3_bucket.project_bucket.id}"

    forwarded_values {
      query_string = false
      headers = ["Origin"]

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl = 0
    default_ttl = 3600
    max_ttl = 86400
    compress = true
  }
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  tags = {
    Name = "${var.project_bucket}"
    Environment = "Stage"
  }
}
