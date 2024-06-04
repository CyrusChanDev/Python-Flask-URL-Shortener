terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

# VPC
resource "aws_vpc" "url_shortener_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "url_shortener_VPC"
  }
}

# Subnet
resource "aws_subnet" "subnet" {
  vpc_id            = aws_vpc.url_shortener_vpc.id
  availability_zone = "us-west-2a"
  cidr_block        = "10.0.10.0/24"
  tags = {
    Name = "url_shortener_VPC_SUBNET"
  }
}

# Internet gateway
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.url_shortener_vpc.id

  tags = {
    Name = "url_shortener_VPC_IGW"
  }
}

# Route table
resource "aws_route_table" "routes" {
  vpc_id = aws_vpc.url_shortener_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "url_shortener_VPC_ROUTETABLE"
  }
}

# Route table association
resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.subnet.id
  route_table_id = aws_route_table.routes.id
}

# Security group
resource "aws_security_group" "allow_ssh_http" {
  name        = "allow_ssh_http"
  description = "Allow SSH and HTTP inbound traffic, allow all outbound"
  vpc_id      = aws_vpc.url_shortener_vpc.id

  ingress {
    description      = "SSH to EC2"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  ingress {
    description      = "HTTP to EC2"
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_ssh_http"
  }
}

# Define the EC2 instance
resource "aws_instance" "app_server" {
  subnet_id                   = aws_subnet.subnet.id
  ami                         = "ami-03c983f9003cb9cd1"     # Ubuntu server 22.04 LTS 64-bit
  instance_type               = "t2.nano"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.allow_ssh_http.id]

  tags = {
    Name = "vpc_shortener_app"
    Service = "vpc_shortener_app"
  }
}