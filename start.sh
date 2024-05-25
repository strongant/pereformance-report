#!/bin/bash

# 设置变量
REPO_URL="https://github.com/strongant/pereformance-report.git"
PROJECT_DIR="/root"
VENV_DIR="$PROJECT_DIR/venv"
SERVICE_NAME="flaskapp"

# 检查并创建项目目录
if [ ! -d "$PROJECT_DIR" ]; then
  mkdir -p "$PROJECT_DIR"
fi

# 克隆或更新仓库
if [ -d "$PROJECT_DIR/.git" ]; then
  cd "$PROJECT_DIR"
  git pull origin main
else
  git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# 设置虚拟环境
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 安装依赖项
pip install -r requirements.txt

# 迁移数据库（如果需要）
# flask db upgrade

# 停用虚拟环境
deactivate

# 创建 systemd 服务文件
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"

if [ ! -f "$SERVICE_FILE" ]; then
  sudo bash -c "cat > $SERVICE_FILE" << EOL
[Unit]
Description=Flask Application
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
EOL
fi

# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启动并启用服务
sudo systemctl start $SERVICE_NAME
sudo systemctl enable $SERVICE_NAME

echo "Deployment completed and service started."
