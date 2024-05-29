FROM python:3.10

# Set working directory in the container
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

EXPOSE 9091

CMD ["python3", "main.py"]