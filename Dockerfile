# 1. Start from the official Microsoft Playwright image.
# This image comes with Python and all system dependencies for Playwright pre-installed.
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the Python requirements file into the container
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port your FastAPI server will run on
EXPOSE 8000

# 7. Define the command to run your application when the container starts
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
