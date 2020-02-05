# This file is provided as an example only and is not sutible for use in a production environment
# This script should be used as a GCP Cloud Run container and used to allow uploads to a GCS
# buicket. Run.py creates a local copy of a service account key file on the container from a
# GCP Secret using the Secret Manager service. The local key is required by the Cloud Storage
# python library used in the main.py script to generate the SingedURL used to upload files to GCS

import os
from google.cloud import secretmanager_v1beta1 as secretmanager

# Function to create a new service key file
def KeyGen(keyfile):
    # Connect to the secret manager in GCP to generate the local copy of the GCP Service Account key file
    client = secretmanager.SecretManagerServiceClient()
    # Variables for the GCP secret and project names defined in the Dockerfile
    secret_name = os.environ['GCP_SECRET']
    project_id = os.environ['GCP_PROJECT']
    # Define the path and version of the secret. Update the version number if needed
    secret_name = f"projects/{project_id}/secrets/{secret_name}/versions/1"
    response = client.access_secret_version(secret_name)
    secret_string = response.payload.data.decode('UTF-8')
    print('Secret accessed and generating service key')
    # Write the contents of the GCP secret to a local json file. The key file and path is passed from the 'GCP_KEYFILE' environment variable defined in the Dockerfile
    with open(keyfile, 'w') as outfile:
        outfile.write(secret_string)
    print('Service account key created')

if __name__ == '__main__':
    # Get the local key file name and path from the GCP_KEYFILE environment variable defined in the Dockerfile
    svckeyfile = os.environ['GCP_KEYFILE']
    # See if the service account key kile exists and if not create it from the GCP Cloud Secret
    try:
        with open(svckeyfile, 'r') as fh:
            print('Service account key exists. Launching webservice.')
    except FileNotFoundError:
        print('Service account key does not exist. Creating service account key.')
        KeyGen(svckeyfile)
    # Starting the webservice using the gunicorn webserver, with one worker process and 8 threads.
    # For environments with multiple CPU cores, increase the number of workers to be equal to the cores available.
    os.system('exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app')
