# Python Flask URL Shortener  

## Background and Purpose

This personal project is a URL shortener built using Python's Flask library. 

Built for the purpose to allow me to practice infrastructure as code using Terraform and configuration management with Ansible. I use Docker to ensure the predictable behaviour across a variety of machines both on the cloud and on-premises. The CI/CD of choice is GitHub Actions. 

While the core functionality is a URL shortener, the primary focus is on the Ops side. Regarding of operations or development, modularity is at the top of my mind and variables throughout are not hardcoded and can be configured in `./configs`.

---

## Installation

#### Local machine:

Please ensure the following software are installed:
- Python
- Python Flask library
- Docker (and Docker Compose)
- Terraform
- Ansible


#### AWS Cloud:
No manual configuration needed. Infrastructure provisioning, machine configuration, and application setup is all handled through Terraform, Ansible, and Docker.

Note: Please ensure AWS credentials are configured where required so that Terraform and Ansible are able to talk to the AWS resources in your account. NEVER use the root user in your AWS account, instead create a user with least privilege. This setup is a one-time process.

---

## Usage

There are two ways to run the code. On your own local machine or in AWS cloud via EC2 instances (the functionality is the exact same on either platform). The instructions will assume the default state where variables in `./configs` have not been modified.

#### Local machine: 

Please navigate to where the repository has been cloned on your machine and run the following command in the terminal in the same directory where the Docker Compose file is located.

`docker-compose -f docker-compose.yaml --env-file ./configs/.env up --build`

When you see the message `* Running on https://127.0.0.1:9091` the application is now up and fully operational. You can now access the site at `http://localhost:9091` in your web browser.

#### AWS Cloud:

Navigate to `./terraform` and run the following command in terminal:

`terraform apply -var-file=terraform.tfvars`

When you see the output of the provisioned EC2 instance's public IPv4 IP address, you will know that this step is complete.  
  
  Please wait 30 seconds to ensure that the EC2 instance is fully booted up and then run this command in `./ansible` to allow Ansible to configure the machine accordingly — including setting up the application via Docker Compose:

`ansible-playbook -i dynamic_inventory.py playbook.yaml` 

`dynamic_inventory.py` will automatically retrieve the provisioned EC2's machine public IPv4, you do NOT need to manually edit any files. If you see an error, you will need to use `chmod` and make the `dynamic_inventory.py` executable so that Ansible has the necessary permissions to treat it as a dynamic inventory file.

Ansible will let you know when it has completed its magic and then you can access the site at `http://{your_ec2_instance_public_ipv4_ip}:9091` 

---

## Credits and Contact

All work in this GitHub repository is completed by me - Cyrus Chan. With the exception of `./utils/wait-for-it.sh` which I did not develop, the original work can be found here: https://github.com/vishnubob/wait-for-it/blob/master/wait-for-it.sh
