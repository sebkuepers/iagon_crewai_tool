import os
import requests

from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# Load environment variables
IAGON_API_KEY = os.getenv("IAGON_API_KEY")
IAGON_PASSWORD = os.getenv("IAGON_PASSWORD")
BASE_URL = "https://gw.iagon.com/api/v2/storage"

class GetDirectoryIdInput(BaseModel):
    """Input schema for GetDirectoryIdTool."""
    directory_name: str = Field(..., description="Name of the directory to find")
    visibility: str = Field(default="private", description="Visibility of the directory (private or public)")

class UploadFileInput(BaseModel):
    """Input schema for UploadFileTool."""
    file_path: str = Field(..., description="Path to the file to upload")
    visibility: str = Field(default="private", description="Visibility of the upload (private or public)")
    file_name: str = Field(default=None, description="Optional custom name for the uploaded file")
    directory_name: str = Field(default=None, description="Optional directory name to upload to")


class IAGONUploadFileTool(BaseTool):
    name: str = "Upload File"
    description: str = "Uploads a file to Iagon storage, optionally to a specified directory."
    args_schema: Type[BaseModel] = UploadFileInput

    def _get_directory_id(self, directory_name: str, visibility: str) -> str:
        headers = {"x-api-key": IAGON_API_KEY}
        params = {
            "visibility": visibility,
            "listingType": "index"
        }

        response = requests.get(f"{BASE_URL}/directory", headers=headers, params=params)
        
        if response.status_code == 200:
            directories = response.json().get("data", {}).get("directories", [])
            for directory in directories:
                if directory.get("directory_name") == directory_name:
                    return directory["_id"]
        return None

    def _run(self, file_path: str, visibility: str = "private", file_name: str = None, directory_name: str = None) -> str:
        headers = {"x-api-key": IAGON_API_KEY}
        
        payload = {
            "filename": file_name if file_name else os.path.basename(file_path),
            "visibility": visibility,
        }

        if directory_name:
            directory_id = self._get_directory_id(directory_name, visibility)
            if directory_id:
                payload["directoryId"] = directory_id
            else:
                return f"Directory '{directory_name}' not found"

        if visibility == "private" and IAGON_PASSWORD:
            payload["password"] = IAGON_PASSWORD

        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                response = requests.post(f"{BASE_URL}/upload", headers=headers, files=files, data=payload)
            
            if response.status_code == 200:
                return f"File successfully uploaded: {response.json()}"
            return f"Upload failed with status {response.status_code}: {response.text}"
            
        except Exception as e:
            return f"Upload failed with error: {str(e)}"
        

class IAGONGetDirectoryIdTool(BaseTool):
    name: str = "Get Directory ID"
    description: str = "Retrieves the ID of a specified directory from Iagon storage."
    args_schema: Type[BaseModel] = GetDirectoryIdInput

    def _run(self, directory_name: str, visibility: str = "private") -> str:
        headers = {"x-api-key": IAGON_API_KEY}
        params = {
            "visibility": visibility,
            "listingType": "index"
        }

        response = requests.get(f"{BASE_URL}/directory", headers=headers, params=params)
        
        if response.status_code == 200:
            directories = response.json().get("data", {}).get("directories", [])
            for directory in directories:
                if directory.get("directory_name") == directory_name:
                    return directory["_id"]
        return f"Directory '{directory_name}' not found or error occurred."
