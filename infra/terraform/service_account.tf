resource "google_service_account" "default" {
  account_id   = var.service-account
  display_name = "Service Account"
}

resource "google_project_iam_member" "default_service_account_artifact_registry_grant" {
  project = var.project
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.default.email}"
}

resource "google_project_iam_member" "default_service_account_firestore_grant" {
  project = var.project
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.default.email}"
}

