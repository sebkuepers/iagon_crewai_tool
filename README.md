# IAGON Tools Documentation

## Description
These tools are designed to interact with the Iagon storage service, providing functionality to retrieve directory IDs and upload files. The tools utilize the Iagon Storage API to manage files and directories in both private and public visibility modes. The following sections describe how to use the IAGONGetDirectoryIdTool for retrieving directory IDs and the IAGONUploadFileTool for uploading files to the Iagon storage service.

## Installation
To incorporate this tool into your project, follow the installation instructions below:
```shell
# Clone the repository into your CrewAI project's tools directory
git clone https://github.com/sebkuepers/iagon_crewai_tool.git your_project/tools/
```

## Example
The following example demonstrates how to initialize the tool and execute a search with a given query:

```python
# Import the tools from your project structure
from your_project.tools.iagon_tool import IAGONUploadFileTool

# Initialize the tool for internet searching capabilities
tool = IAGONUploadFileTool()
```

## Steps to Get Started
To effectively use the IAGON tools, follow these steps:

1. **API Key Acquisition**: Create an account on [Iagon](https://iagon.com/) and obtain your API key from the dashboard. Click on your Profile Picture, go to Settings and then generate a Personal Access Token.
2. **Environment Variables**: Set up the following environment variables:
   - `IAGON_API_KEY`: Your Iagon Personal Access Token for authentication
   - `IAGON_PASSWORD`: Your password for private file encryption (optional, only needed for private uploads)


## How to use the tools
Currently, the tool only supports uploading files to the Iagon storage service.
The following parameters are supported:
- `file_path`: The path to the file you want to upload
- `visibility`: The visibility of the upload (defaults to "private", can be "private" or "public")
- `file_name`: Optional custom name for the uploaded file
- `directory_name`: Optional directory name to upload the file to

You can simply instruct the agent in natural language to upload a file to the Iagon storage service,
and if the file should be uploaded to a specific directory, you can specify the directory name. (is has to exist already)

The visibility can be set to "private" (default) or "public", depending on whether you want the file to be accessible to everyone or only you.
