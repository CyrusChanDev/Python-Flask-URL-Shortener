# instance.tf -----

key_name = "PersonalProject.pem"
public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCMe6z85o19tnOhKroCD/AHKDAA9dfNUH+tXyZN0dGCejmKTMwWbXMYBNnWdyIwoP+PGzob6kMvNtlP0i3Y2HSa0IHRRRQ09/K1+eR1buFVFLAuidsOsKw3opVaY/jgeOe6GXrOZP1QHu6r0jhy3PZjbJwgIEdzk+F/YOuzYfMAC7uskG14OBUIPjOHpd0pW8NDCLg5aSmS9xlfJNGc6zc/6hWi2L/r5GAI9aDFBUylyD+Cd2Uuzco/z02wH+DYjdNbNw1j6hAaBxON+Th55Y+mG0LyshKcp2Jvo88RxpkOiEV27dL1ldZIcMRNQR9mFUghHD5/NsxPIwMwvLAKUcyD"
ami = "ami-03c983f9003cb9cd1" # Ubuntu server 22.04 LTS 64-bit
instance_type = "t2.micro"
associate_public_ip_address = true

# vpc.tf -----

vpc_cidr_block = "10.0.0.0/16"
subnet_availability_zone = "us-west-2a"
subnet_cidr_block = "10.0.10.0/24"
route_table_cidr_block = "0.0.0.0/0"

# main.tf -----

region = "us-west-2"