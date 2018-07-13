# Log Management Tool
This is a simple prototype developed like a ELK Stack. It was developed using Python3, PyMongo as the backend, and AngularJS as the frontEnd. You can compare those ELK Stack module structure with this prototype,
* Elasticsearch - elasticAPI.py
* Logstash - logLinesToEAPIMapper.py
* Kibana - public/index.html

## Instructions 

1. Please clone this repository and install the required modules using this command
```
pip install -r requirements.txt
```
2. Open the `config.json` file and change the ports if you need. There will be two componets which are wanted to run at the same time to test this prototype.
3. Open a terminal and navigate to this directory, then start the `elasticAPI.py` componet by typing `python elasticAPI.py` command (Don't close it until the end).
4. Open another terminal and navigate to this directory, then start the `logLinesToEAPIMapper.py` component by typing `python logLinesToEAPIMapper.py` command (Don't close it until the end).
5. You have started the two main components which are needed to run this prototype.
6. I have included some sample logs from Nginx server in the sampleLogs folder. So you can run this python script to load that logs from the text file and send it to logLinesTOEAPIMapper component. Then the mapper component will create a mapping for the logLine, and send it to elasticAPI component to store in the database. 
```
python exampleApps/insertLogs.py  ` 
```
7. `requstSamples` module inside the exampleApps contains some sample requests to fetch the loglines from the server(elasticAPI component). You can try this following command,
```
python exampleApps/requstSamples.py  ` 
```
8. Go to the public folder in this repository, and Open the `index.html` in your broswer (make sure, you have the internet connection, since the required dependencies for this view are connected with online cdns). You can get a view to select the date and fetch the logs (Logs from the sampleLog file dated between 2018/07/04 to 2018/07/12)

![enter image description here](https://suthagar.inncaps.com/img/Selection_171.png)

