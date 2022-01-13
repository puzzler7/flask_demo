# Flask Demo for ECE 458
### Written by Maverick Chung

If running this on a server (like a VCM), replace `localhost` below with the server IP or hostname.

## Run without Docker
* Clone the repo and navigate inside it
* Install Python 3
* `pip3 install -r requirements.txt`
* `flask run --host 0.0.0.0`
* Visit `http://localhost:5000`

## Run with Docker
* Install Docker and Docker Compose
* Clone the repo
* `sudo docker-compose up --build`
* Visit `http://localhost:5000`