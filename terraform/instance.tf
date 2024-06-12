# Pass public key to instance so we can connect with our pre-existing private key
resource "aws_key_pair" "deploy_key" {
  key_name   = var.key_name
  public_key = var.public_key
}

# Define the EC2 instance
resource "aws_instance" "app_server" {
  subnet_id                   = aws_subnet.subnet.id
  ami                         = var.ami
  instance_type               = var.instance_type
  associate_public_ip_address = var.associate_public_ip_address
  vpc_security_group_ids      = [aws_security_group.allow_ssh_http.id]
  key_name = aws_key_pair.deploy_key.key_name

  tags = {
    Name = "vpc_shortener_app"
    Service = "vpc_shortener_app"
  }
}