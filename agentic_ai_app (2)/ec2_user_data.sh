
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
