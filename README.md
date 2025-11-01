
Agentic AI Streamlit App Deployment Guide
This guide provides step-by-step instructions for deploying the Agentic AI Streamlit App on an Amazon EC2 instance. The app supports multi-source data ingestion, prompt analysis, and integrates with Amazon Bedrock, OpenSearch, and Redshift.


F4C2 Project Structure
agentic_ai_app/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── ec2_user_data.sh           # EC2 bootstrap script
├── utils/
│   └── auth.py                # Basic password authentication
├── nlp/
│   └── preprocess.py          # Text preprocessing for NLP
├── opensearch/
│   └── mapping.py             # OpenSearch index creation




F4DD Step-by-Step Deployment Instructions
1. Launch an EC2 Instance

Use Ubuntu 22.04 LTS
Choose instance type (e.g., t2.medium or higher)
Configure security group to allow inbound traffic on port 80 and 8501
2. Attach EC2 Bootstrap Script
Paste the contents of ec2_user_data.sh into the User Data section:
#!/bin/bash
apt update -y
apt install -y docker.io git
systemctl start docker
systemctl enable docker

cd /home/ubuntu
git clone https://github.com/your-username/agentic_ai_app.git
cd agentic_ai_app
docker build -t agentic-ai-app .
docker run -d -p 80:8501 agentic-ai-app


3. Access the App

After EC2 boots, visit http://<EC2_PUBLIC_IP> in your browser
Enter password (admin123) to access the app


F4C8 Features Included
F4C2 File Ingestion

CSV, Excel, JSON, TXT, PDF
F4C1 Database Access

Amazon DynamoDB
Amazon Redshift
F4E1 API Data Source

Fetch and analyze data from internal/external APIs
F9E0 NLP Preprocessing

Text cleaning and normalization
F916 Amazon Bedrock Integration

Claude v2 via Bedrock Runtime
Bedrock Agent orchestration
Bedrock Knowledge Base support
F50D OpenSearch Integration

Index creation and semantic search setup


F512 Authentication

Basic password protection via auth.py
Default password: admin123


F4DA Requirements
Install dependencies manually (if not using Docker):
pip install -r requirements.txt




F4E6 Notes

Replace your-agent-id, your-alias-id, and your-knowledge-base-id in app.py with actual Bedrock resource IDs
Ensure IAM roles attached to EC2 have permissions for Bedrock, DynamoDB, Redshift, and OpenSearch


F4E7 Contact
Maintainer: Deepak Sinha (Cognizant) Location: Bromley, KE Role: Architect - Technology


For issues or contributions, please open a pull request or issue on GitHub.
