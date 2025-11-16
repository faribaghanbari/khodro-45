FROM mcr.microsoft.com/playwright/python:v1.49.1-jammy

# Set working directory
WORKDIR /usr/src/app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create reports directory
RUN mkdir -p reports/html-report reports/junit test-results

# Default command to run tests
CMD ["pytest", "--html=reports/html-report/index.html", "--self-contained-html", "--junitxml=reports/junit/results.xml"]

