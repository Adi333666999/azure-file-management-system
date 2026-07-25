# Azure File Management System

## Overview

Azure File Management System is a cloud-based web application built using Flask and Microsoft Azure. It allows users to upload, view, download, and delete files while storing the actual files in Azure Blob Storage and maintaining metadata in Azure SQL Database.

The application is deployed on Azure App Service and demonstrates an end-to-end cloud architecture.

---

## Features

- Upload files
- Store files in Azure Blob Storage
- Save metadata in Azure SQL Database
- View uploaded files
- Download files
- Delete files
- Automatic synchronization between Blob Storage and SQL Database
- Hosted on Azure App Service

---

## Azure Services Used

- Azure App Service
- Azure Blob Storage
- Azure SQL Database
- Application Insights

---

## Technology Stack

### Backend

- Python
- Flask

### Database

- Azure SQL Database

### Storage

- Azure Blob Storage

### Cloud Platform

- Microsoft Azure

---

## Project Architecture

User

↓

Azure App Service (Flask)

↓

Azure Blob Storage ←→ Azure SQL Database

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /upload | Upload file |
| GET | /files | List uploaded files |
| GET | /download/<id> | Download file |
| DELETE | /file/<id> | Delete file |

---

## Project Workflow

1. User uploads a file.
2. Flask receives the request.
3. File is stored in Azure Blob Storage.
4. Metadata is stored in Azure SQL Database.
5. Users can list, download, or delete files.

---

## Future Enhancements

- Azure Functions
- Azure Front Door
- Azure Monitor integration
- CI/CD using GitHub Actions
- Authentication using Microsoft Entra ID

---

## Author

Aditya Patil
