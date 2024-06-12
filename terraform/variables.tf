variable "key_name" {
    description = "The name of the key pair"
    type = string
}

variable "public_key" {
    description = "The public key to use for SSH access"
    type = string
}

variable "ami" {
    description = "The AMI ID for the EC2 instance"
    type = string
}

variable "instance_type" {
    description = "The type of AWS instance to use"
    type = string
}

variable "associate_public_ip_address" {
    description = "Assign EC2 instance a public IP address" 
    type = bool 
}