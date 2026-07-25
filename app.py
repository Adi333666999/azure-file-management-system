from flask import Flask, request, render_template
from azure.storage.blob import BlobServiceClient
import pymssql
from flask import jsonify
from flask import send_file
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Azure Storage Connection String
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

conn = pymssql.connect(
    server=SQL_SERVER,
    user=SQL_USERNAME,
    password=SQL_PASSWORD,
    database=SQL_DATABASE,
    port=1433,
    login_timeout=30,
    timeout=30,
    tds_version='7.4'
)

cursor = conn.cursor()

cursor.execute("""
IF OBJECT_ID('UploadedFiles', 'U') IS NULL
BEGIN
    CREATE TABLE UploadedFiles (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        FileName NVARCHAR(255),
        BlobUrl NVARCHAR(MAX),
        UploadedAt DATETIME DEFAULT GETDATE()
    )
END
""")

@app.route("/files", methods=["GET"])
def get_files():
    cursor.execute("""
        SELECT Id, FileName, BlobUrl, UploadedAt
        FROM UploadedFiles
        ORDER BY UploadedAt DESC
    """)

    rows = cursor.fetchall()

    files = []
    for row in rows:
        files.append({
            "id": row[0],
            "file_name": row[1],
            "blob_url": row[2],
            "uploaded_at": str(row[3])
        })

    return jsonify(files)

@app.route("/file/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):

    cursor.execute(
        "SELECT FileName FROM UploadedFiles WHERE Id=%s",
        (file_id,)
    )

    row = cursor.fetchone()

    if not row:
        return {"message": "File not found"}, 404

    filename = row[0]

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=filename
    )

    blob_client.delete_blob()

    cursor.execute(
        "DELETE FROM UploadedFiles WHERE Id=%s",
        (file_id,)
    )

    conn.commit()

    return {
        "message": f"{filename} deleted successfully."
    }

@app.route("/download/<int:file_id>", methods=["GET"])
def download_file(file_id):

    cursor.execute(
        "SELECT FileName FROM UploadedFiles WHERE Id=%s",
        (file_id,)
    )

    row = cursor.fetchone()

    if not row:
        return {"message": "File not found"}, 404

    filename = row[0]

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=filename
    )

    stream = blob_client.download_blob()

    return send_file(
        BytesIO(stream.readall()),
        as_attachment=True,
        download_name=filename
    )

conn.commit()

container_name = "uploads"

blob_service_client = BlobServiceClient.from_connection_string(
    AZURE_STORAGE_CONNECTION_STRING
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]

    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=file.filename
    )

    blob_client.upload_blob(file, overwrite=True)

    blob_url = blob_client.url

    cursor.execute(
        """
        INSERT INTO UploadedFiles (FileName, BlobUrl)
        VALUES (%s, %s)
        """,
        (file.filename, blob_url)
    )

    conn.commit()

    return f"<h3>{file.filename} uploaded successfully!</h3>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
