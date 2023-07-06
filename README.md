# Prerequisites

> Install Docker
> Install Colima (only for mac is required)


# Build

$ docker image build -t flask_docker .


# Run

$ docker run -p 8000:8000 -d flask_docker
