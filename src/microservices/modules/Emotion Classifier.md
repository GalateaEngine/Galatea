# Galatea Emotion Classification Module

This module serves an emotion classification engine, it can also be used as a module
**Requires Python 3**
### Usage (Module)
```
from Galatea.microservices.modules.emotion.classifier import classify as classify_emotion

classify_emotion("i hate this place, i wanna go home!")
>>> 'hate'

classify_emotion("i wouldn't recommend this product to anyone",True)
>>>[('anger', 1.6071389940508387e-35),
 ('boredom', 2.2929012345679012e-35),
 ('surprise', 1.1813205360300711e-30),[...]
```
##### Arguments
- **text**(string): Text to be classified
- **full_results**(bool)(Optional, False by default): 
    - if **True** entire output, ordered by likehood (array)
    - if **Flase** returns more likely classification (string) (ex, 'bored')


----
### Usage (Microservice)
Start with `python3 ./server.py`
#### API
- **/classify** : Classify a text
    -  **Arguments**
        -   **text** (string): Text you want to classify      
    - **Example**
        - `<your_url>/classify?text=Hey there!`
    - **Returns**
         - ( json )`{"emotion":"boredom"}`
- **/train**: Train the classifier with new data, also adds to dataset
    -  **Arguments**
        -   **json** 
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
         - ( json )`{},status = 201`
- **/save**: Save the newly added training samples
    -  **Arguments**
        -   **key** (string): The key you defined in config as `secret_key` (Default: 'galatea123') 
    - **Example**
        - `<your_url>/save?key=galatea123`
    - **Returns**
         - ( text ) `Sucessfully saved : 15 items!`
- **/serve**: Download the lastest dataset
    -  **Arguments**
        -   **key** (string): The key you defined in config as `secret_key` (Default: 'galatea123') 
    - **Example**
        - `<your_url>/serve?key=galatea123`
    - **Returns**
         - ( file ) `<your dataset>`

- **/heartbeat**: Checks status of microserver
    -  **Arguments**
    - **Example**
        - `<your_url>/heartbeat`
    - **Returns**
         - ( json ) `{"status":"alive"}`

#### Config (config.json)
- **"database_name"**(string): The name of your database file
- **"microservice_port"**(int): The port of your microservice
- **"microservice_host"**(string): The ip of your microservice
    - **Note**:
        - Using (127.0.0.1) will make the service only locally accessible
        - Using (0.0.0.0) will make the service accessible to your entire network
- **"debug"**(bool): If you want to see debug data
- **"logger_name"**(string): The name of your logger
- **"server_workers"**(int): The number of workers for this microservice
    - **Note**: If you dont know how many to put check your cores, by default 2 
- **"gzip_enabled"**(bool): Should we gzip the responses?
    - **Note**: This makes minimal impact in your performance and decreases transfer sizes, make it true if you have limited bandwidth
- **"load_checkpoint_database"**(bool): Should we load a checkpoint of the database?
    - **Note**: if false you will need to train the model from scratch
- **"secret_key"**(string): Your private key for auth in your server
