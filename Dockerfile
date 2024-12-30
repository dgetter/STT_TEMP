# Use the official Azure Functions Python base image for Python 3.9
FROM mcr.microsoft.com/azure-functions/python:4-python3.9

# Azure Functions specific settings
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Expose the default port
EXPOSE 80

# Copy the Function App code into the image
COPY . /home/site/wwwroot

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r /home/site/wwwroot/requirements.txt
