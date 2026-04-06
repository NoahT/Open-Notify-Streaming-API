variable "project" {
  default = "open-notify"
}

variable "vpc-network-name" {
  default = "iss-network"
}

variable "region" {
  default = "us-east1"
}

variable "availability-zone" {
  default = "us-east1-b"
}

variable "service-account" {
  default = "open-notify-service-account"
}

variable "container-cluster-node-count" {
  default = 3
}

variable "container-node-pool-machine-type" {
  default = "e2-small"
}

variable "vm-instance-boot-disk" {
  default = "cos-cloud/cos-stable"
}

variable "firestore-database-name" {
  default = "open-notify-staging"
}

variable "artifact-registry-docker-repository-name" {
  default = "open-notify"
}

