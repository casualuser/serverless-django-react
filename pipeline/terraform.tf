provider "aws" {
  region = "ap-southeast-2"
}

terraform {
  backend "s3" {
    bucket = "unsw-pvce-terraform-states"
    key = "eia003.tfstate"
    region = "ap-southeast-2"
    encrypt = "true"
  }
}
