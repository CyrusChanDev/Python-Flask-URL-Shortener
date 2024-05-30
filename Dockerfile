FROM python:3.10

# Set working directory in the container
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# depends_on in docker-compose is not sufficient to determine the actual status of the database service within the container.
RUN chmod +x /app/utils/wait-for-it.sh 

EXPOSE 9091
