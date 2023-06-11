# Weather Fetcher

## General Instructions

1. Clone the Repository:
   ```shell
   git clone https://github.com/Akash1590/weather_fetcher.git
2. Automatic Creation of CSV Folder:  
  By running the project, the CSV folder will be automatically created if there are no permission issues.
  If you encounter any permission issues, manually create a folder named "csv" inside the "weather_fetcher" folder.  
  By running the project, the CSV folder will be automatically created if there are no permission issues.
  If you encounter any permission issues, manually create a folder named "csv" inside the "weather_fetcher" folder.
3. Amazon AWS Data Storage:  
   If you want to use Amazon AWS for your data storage:  
   - Rename the "amazon_credentials.txt" file to "amazon_credentials.py".


## Manual Project Execution  
1. Install Dependencies:
Run the following command to install the project dependencies from the requirements.txt file:
   ```shell 
   pip install -r requirements.txt
   ```
2. Run the Project:  
   Execute the following command to run the project:
   ```shell 
   python index.py
   ```
3. Access the Project:
   The project will run on: http://localhost:5000/
   
## Running the Project with Docker
Requirements: Docker  
1.Build Docker Image:  
  Run the following command to build the Docker image:
  ```shell
  docker build -t <your-docker-image-name> .
  ```  
2. Run the Docker Container:
   Execute the following command to run the Docker container:
   ```shell
   docker run -d -p 5000:5000 <your-docker-image-name>
   ```
   




