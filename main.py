# This file is provided as an example only and is not sutible for use in a production environment
# This script should be used as a GCP Cloud Run container and used to allow uploads to a GCS
# buicket. The main.py script renders the signedurl.html page located in the templates folder
# and generates the temporary signedURL used to upload the user provided file to a GCS bucket

from flask import Flask, render_template, request, Response,  send_from_directory, abort, redirect, jsonify, session
import os
import datetime
from google.cloud import storage


bucketName = os.environ.get('GCP_BUCKET')
svckeyfile = os.environ['GCP_KEYFILE']
client = storage.Client.from_service_account_json(svckeyfile)
bucket = client.get_bucket(bucketName)
app = Flask(__name__, static_url_path='')


@app.route('/public/<path:path>')
def send_file(path):
    return send_from_directory('public', path)


@app.route('/getSignedURL')
def getSignedURL():
    # Creating the upload signedURL. Change the experation time in minutes if needed
    filename = request.args.get('filename')
    action = request.args.get('action')
    blob = bucket.blob(filename)
    url = blob.generate_signed_url(
        expiration=datetime.timedelta(minutes=60),
        method=action, version="v4")
    return url


@app.route('/')
def signedurl():
    return render_template('signedurl.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
