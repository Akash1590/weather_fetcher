# Use a python base image

FROM python

# Working Directory

WORKDIR /app

# Copy the requirements file

COPY requirements.txt .

# Install dependencies

RUN pip install --no-cache-dir -r requirements.txt

# copy the flask project files

COPY . .

# Port

EXPOSE 5000

# Set the command to run the FLASK app
CMD ["python", "index.py"]