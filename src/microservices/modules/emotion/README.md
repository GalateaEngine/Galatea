# Galatea Emotion Classification Module
![](https://img.shields.io/badge/Passed-Integration%20tests-green.svg?&style=for-the-badge) ![](https://img.shields.io/badge/passed-unit%20tests-green.svg?&style=for-the-badge) 

-----
### Summary
This module serves an emotion classification engine, it can be used as a module or a microservice.

![](https://img.shields.io/badge/%20-microservice-yellow.svg?&style=for-the-badge) ![](https://img.shields.io/badge/%20-module-red.svg?&style=for-the-badge) 


-----
## Tech

![](https://img.shields.io/badge/Python-+3.5-yellow.svg?&style=for-the-badge) 

### Dependencies
![](https://img.shields.io/badge/Machine%20Learning-skLearn-orange.svg?&style=for-the-badge) ![](https://img.shields.io/badge/algorithm-naive%20bayes-yellow.svg?&style=for-the-badge)

![](https://img.shields.io/badge/Server%20Framework-sanic-blue.svg?&style=for-the-badge) 


```
sanic_limiter==0.1.3
sanic==0.7.0
sanic_compress==0.1.1
Sanic_Cors==0.9.3
scikit-learn==0.19.1
pytest==3.5.1
```
----
### Integration and Unit Tests
```
pytest unit_tests.py
pytest integration_tests
```
![](https://img.shields.io/badge/Passed-Integration%20tests-green.svg?&style=for-the-badge) ![](https://img.shields.io/badge/passed-unit%20tests-green.svg?&style=for-the-badge) 
----
### Usage (Module)
```
from classifier import classify as classify_emotion

classify_emotion("im felling great")
>>> 'happiness'
```
##### Arguments
- **text**(string): Text to be classified


----
### Usage (Microservice)
Start with `python ./server.py`
#### API
- **/ (GET)** : Classify a text
    -  **Arguments**
        -   **text** (string): Text you want to classify      
    - **Example**
        - `<your_url>/?text=Hey there!`
    - **Returns**
         - ( json )`{"emotion":"boredom"}`
- **/add (POST)**: Adds to dataset
    -  **Arguments (JSON)**
        - **text** (string): Text to train 
            - **emotions**: Contains the following emotions
                - 'anger', 'boredom', 'empty', 'enthusiasm', 'fear', 'fun', 'happiness', 'hate', 'love', 'neutral', 'relief', 'sadness', 'surprise', 'worry' 
                - {**"emotion"** : **"float (1-0)"**} pairs
         - **Example**
            - `<your_url>/train  `
               - json:
                 - `{
  "text": "Im not feeling",
  "emotions": {
    "anger": "0.0",
    "boredom": "0.01",
    "empty": "0.02",
    "enthusiasm": "0.03",
    "fear": "0.04",
    "fun": "0.05",
    "happiness": "0.06",
    "hate": "0.07",
    "love": "0.08",
    "neutral": "0.09",
    "relief": "0.1",
    "sadness": "0.11",
    "surprise": "0.12",
    "worry": "0.13"
  }
}`
    - **Returns**
        - ( text )` 'ok' (status = 201)`
- **/download_dataset**: Downloads the dataset
    -  **Note**
        -   **--allow_download_dataset** (argument): Needs to be true
    - **Example**
        - `<your_url>/download_dataset`
    - **Returns**
         - ( file ) `<your dataset>`

- **/heartbeat**: Checks status of microserver
    - **Example**
        - `<your_url>/heartbeat`
    - **Returns**
         - ( json ) `{"status":"alive"}`
-----
#### CONFIG (with parameters)
```
$ python server.py -h
usage: server.py [-h] [-C path/to/config] [-P XXXX] [-H X.X.X.X] [-W X]
                 [-D true/false] [-gzip true/false] [-a true/false]
                 [-dataset path/to/file] [-download true/false]

Emotion Classification Microservice

optional arguments:
  -h, --help            show this help message and exit
  -C path/to/config, --config_file path/to/config
                        path to the config file
  -P XXXX, --port XXXX  port of the server
  -H X.X.X.X, --host X.X.X.X
                        host of the server (127.0.0.1 for localhost) (0.0.0.0
                        for entire network)
  -W X, --workers X     workers of the server
  -D true/false, --debug true/false
                        debug logging
  -gzip true/false, --gzip_enabled true/false
                        output compression
  -a true/false, --add_dataset true/false
                        allow ingestion of new samples via /add
  -dataset path/to/file, --dataset_file path/to/file
                        where to save the dataset file, only relevant if
                        --add/-a is true
  -download true/false, --allow_download_dataset true/false
                        allow /download_dataset to serve the dataset (defined
                        in --dataset)
```
-----
#### CONFIG (with config file)

- **"port"**(int): The port of your microservice
- **"host"**(string): The ip of your microservice
    - **Note**:
        - Using (127.0.0.1) will make the service only locally accessible
        - Using (0.0.0.0) will make the service accessible to your entire network
- **"debug"**(bool): If you want to see debug data

- **"workers"**(int): The number of workers for this microservice
    - **Note**: If you dont know how many to put check your cores, by default 2 
- **"gzip_enabled"**(bool): Should we gzip the responses?
    - **Note**: This makes minimal impact in your performance and decreases transfer sizes, make it true if you have limited bandwidth
- **"add_dataset"**(bool): Allow /add to recive new dataset samples
- **"allow_download_dataset"**(bool): Allow /download_dataset to download a copy of your dataset

Example config file
```
{
    "port":"5000",
    "host":"0.0.0.0",
    "workers":"2",
    "debug":true,
    "gzip_enabled":true,
    "add_dataset":true,
    "allow_download_dataset":false    
} 
```
