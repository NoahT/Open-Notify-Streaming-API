**kustomize overlays**

This directory contains environment-specific overlays we want to layer in each environment we intend to run our cluster. Each subdirectory has the following:
- `kustomization.yaml`, to define the k8s manifests and configMaps we want to use in each environment.
- `.env` files, containing the environmental variables we want to configure for each environment
- Optional patch files to modify fields on a k8s manifest.
