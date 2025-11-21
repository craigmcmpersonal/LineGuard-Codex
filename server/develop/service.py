import os
import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response, url_for
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage
from azure.storage.blob import BlobServiceClient, ContainerClient, StorageStreamDownloader, BlobClient
from flask_cors import CORS

from develop import constants
from develop import environment
from develop.monitoring.logger import Logger

load_dotenv()

ERROR_KEY: str = "error"
HOST: str = "0.0.0.0"

app: Flask = Flask(__name__)
CORS(
    app,
    expose_headers=[
        constants.HYPERTEXT_TRANSFER_HEADER_KEY_LINK,
        constants.HYPERTEXT_TRANSFER_HEADER_KEY_LOCATION,
    ],
    supports_credentials=True
)

if __name__ == "__main__":
    port_value: Any = environment.try_get_value(environment.KEY_WEB_SERVICE_PORT)
    port: int = int(port_value)
    Logger.instance().info(f"{port}")
    app.run(host=HOST, port=port)
