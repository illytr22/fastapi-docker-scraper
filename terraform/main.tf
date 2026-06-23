provider "aws" {
  region = "eu-central-1" 
}

# 1. 导入你刚刚在 Windows 生成的公钥
resource "aws_key_pair" "scraper_auth" {
  key_name   = "scraper-ec2-key"
  public_key = file("C:/Users/1/.ssh/aws_scraper_key.pub") 
}

# 2. 配置安全组（允许 SSH 和 FastAPI 的 8000 端口通信）
resource "aws_security_group" "scraper_sg" {
  name        = "scraper_security_group"
  description = "Allow SSH, HTTP, and FastAPI traffic"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "FastAPI default port"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# 3. 查找最新的 Ubuntu 22.04 官方镜像
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# 4. 创建免费套餐的 EC2 实例
resource "aws_instance" "scraper_server" {
  ami             = data.aws_ami.ubuntu.id
  instance_type   = "t3.micro" # AWS 免费套餐规格
  key_name        = aws_key_pair.scraper_auth.key_name
  security_groups = [aws_security_group.scraper_sg.name]

  # 服务器启动时，自动执行以下脚本安装 Docker
  user_data = <<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu
              EOF

  tags = {
    Name = "FastAPI-Scraper-Prod"
  }
}