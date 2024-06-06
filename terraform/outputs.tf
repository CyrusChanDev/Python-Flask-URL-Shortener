# Output the public IPv4 address, which is random every time as there's no elastic IP associated
output "ec2_instance_public_ip" {
  value = aws_instance.app_server.public_ip
}