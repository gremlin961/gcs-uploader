# gcs-uploader
Web service for Cloud Run that allows uploading to a GCS bucket. This is a modified version of the GCS File Uploader provided by Matt Cowger at https://github.com/mcowger/gcs-file-uploader

This version uses GCP's Secrets Manager service to provide more security around the GCP service account keys used to create the signedURL for uploads. Instead of including a service account's json key, you can store the key as a secret in the Secret Manager. Run the container in Cloud Run using a service account that has accessor rights to the secret and it will generate a local copy of the key file when the container is launched.

You will want to update the following environment variables in the Dockerfile when you build your image or set them in Cloud Run when you launch the container:

GCP_BUCKET - The name of the bucket you will be uploading files to
GCP_PROJECT - The name of your GCP project
GCP_SECRET - The name of the secret used to store the service account key file
GCP_KEYFILE - The path and name to save the key file to (i.e. /tmp/key.json)

Make sure the service account you run the container as in Cloud Run has access to the secret in Secret Manager. It does not have to be the same service account as key file used to upload the file to GCS.

To use this example code, clone the repo to your GCP cloud shell and update the 4 OS variables in the Dockerfile. To build the image, run the following command, replacing "PROJECT_ID" with name of your project.

docker build -t gcr.io/$PROJECT_ID/uploader . && docker push gcr.io/$PROJECT_ID/uploader:latest
