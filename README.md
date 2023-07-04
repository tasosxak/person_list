# Prerequisites

> Install Docker
> Install Colima (only for mac is required)


# Build

$ docker image build -t flask_docker .


# Run

$ docker run -p 5000:5000 -d flask_docker
