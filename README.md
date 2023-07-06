# Flask CRUD Application

This is a Flask application that allows you to manage persons data.

## Prerequisites

- Docker: Install Docker on your machine.
- Colima (Mac only): Install Colima for Docker management.

## Installation

1. Clone the repository:

`git clone https://github.com/tasosxak/person_list.git`

2. Change into the project directory:

`cd person_list`


## Configuration

- You can configure the application by modifying the `config.py` file. Update the database details, secret key and any other configuration options as needed.

- Create a `.env` file  in the project root directory with the `FLASK_APP` environment variable set to `main.py` and FLASK_RUN_PORT set to `8000`:

```
FLASK_APP=main.py
FLASK_RUN_PORT=8000
```

## Build 

1. If you're running on macOS, start the Colima service by running the following command:

`colima start`

2. Build the Docker image:

`docker image build -t flask_docker .`


## Run

1. Run the Docker container:

`docker run -p 8000:8000 -d flask_docker`

2. Access the application:

Open your web browser and go to  `http://localhost:8000` to access the application.

## License

This project is licensed under the [MIT License](LICENSE).