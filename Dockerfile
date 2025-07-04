# # Use Python 3.11 as base image
# FROM python:3.11-slim

# # Set working directory inside container
# WORKDIR /app

# # Copy user Python script into container
# COPY my_script.py .

# # (Optional) Copy requirements file if available
# COPY requirements.txt .

# # Install dependencies from requirements.txt if available
# RUN if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi

# # Run the user's Python script
# CMD ["python", "my_script.py"]


FROM python:3.11-slim

WORKDIR /app

COPY my_script.py .
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "my_script.py"]
