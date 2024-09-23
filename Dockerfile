FROM python:3.10
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy in the source code
COPY . .

# fastapi dev api.py
CMD ["fastapi", "dev", "./api_app/api.py", "--host", "0.0.0.0"]