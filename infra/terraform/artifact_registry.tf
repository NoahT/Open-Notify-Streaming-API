resource "google_artifact_registry_repository" "open_notify_docker_repository" {
  location      = var.region
  repository_id = var.artifact-registry-docker-repository-name
  description   = "Google artifact registry Docker repository"
  format        = "DOCKER"
}
