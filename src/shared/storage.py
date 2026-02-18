"""
Storage service module blob storage.
This module handles the interaction with storage. This file also responsible to uploadin final markdown report
so they can be accessed permentaly. even after the conatiner shuts down.
"""


from azure.storage.blob import BlobServiceClient
from src.shared.config import settings
import os

class StorageService:
    def __init__(self):
        #  init the connection using string from dotenv
        self.service_client = BlobServiceClient.from_connection_string(
            settings.azure_blob_storage_connection_string
        )
    
        self.container_name = "reports"

        # Ensure that the container exist
        self._ensure_container_exists()

    
    def _ensure_container_exists(self):
        """
        creates the reports container if it doesn't exists
        """

        try:
            container_client = self.service_client.get_container_client(self.container_name)
            if not container_client.exists():
                container_client.create_container()
        except Exception as e:
            print(f"warning checking container : {e}" )
    
    def upload_file(self, file_path : str, destination_name : str) -> str:
        """
        Uploads a local files to azure blob storage.
        args : filepath (local)
        destination name : name it should have in the cloud
        """

        try:
            blob_client = self.service_client.get_blob_client(
                container = self.container_name,
                blob = destination_name
            )

            with open(file_path, "rb") as file:
                blob_client.upload_blob(file, overwrite = True)
            return f"https://{self.service_client.account_name}.blob.core.windows.net/{self.container_name}/{destination_name}"
        except Exception as e:
            print(f" Error uploading to azure :{e}")

