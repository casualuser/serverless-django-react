# ACM resources must be in us-east-1 region in order to be used for CloudFront

resource "aws_acm_certificate" "stage_domain_cert" {
  provider = "aws.us"
  domain_name = "${var.stage_domain}"
  subject_alternative_names = ["*.${var.stage_domain}"]
  validation_method = "DNS"
}

resource "aws_acm_certificate_validation" "stage_domain_cert_validation" {
  provider = "aws.us"
  certificate_arn = "${aws_acm_certificate.stage_domain_cert.arn}"
  validation_record_fqdns = ["${aws_route53_record.stage_cert_validation.fqdn}"]
}

resource "aws_acm_certificate" "prod_domain_cert" {
  provider = "aws.us"
  domain_name = "${var.prod_domain}"
  subject_alternative_names = ["*.${var.prod_domain}"]
  validation_method = "DNS"
}

resource "aws_acm_certificate_validation" "prod_domain_cert_validation" {
  provider = "aws.us"
  certificate_arn = "${aws_acm_certificate.prod_domain_cert.arn}"
  validation_record_fqdns = ["${aws_route53_record.prod_cert_validation.fqdn}"]
}
