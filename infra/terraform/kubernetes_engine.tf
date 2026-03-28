resource "google_service_account" "default" {
  account_id   = var.service-account
  display_name = "Service Account"
}

resource "google_container_cluster" "primary" {
  name     = "cluster-primary"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1
  deletion_protection      = false
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "primary-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.container-cluster-node-count

  node_config {
    preemptible  = true
    machine_type = var.container-node-pool-machine-type

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.default.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}