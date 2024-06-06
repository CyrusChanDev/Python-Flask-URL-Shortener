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