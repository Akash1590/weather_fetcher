General Instructions :
1.Clone the Repository: git clone https://github.com/Akash1590/weather_fetcher.git
2.By running the project, the CSV folder will be automatically created if there are no permission issues.
If, however, you encounter any permission issues, you have to create a folder named "csv" inside the "weather_fetcher" folder
3. If you want to use amazon_aws for your data storage : Rename the amazon_credentials.txt to amazon_credentials.py

If you want to run the project manually :
Run the following command to install the project dependencies from the requirements.txt file: "pip install -r requirements.txt"

Then run the project with : "python index.py"
The project will run on "localhost:5000"

If you want to run the project with docker :
Requirements : docker

Run the command : docker build -t <your docker image name> .
Next Command : docker run -d -p 5000:5000 <your docker image name>




