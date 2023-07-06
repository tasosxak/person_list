# pull the python image
FROM python:3.8-alpine

# copy the requirements file into the container
COPY ./requirements.txt /webserver/requirements.txt

# switch working directory
WORKDIR /webserver

# install the dependencies described in the requirements file
RUN pip install -r requirements.txt

# copy the flask files to the container
COPY . /webserver

# configure the container to run in an executed manner
CMD ["flask", "run", "--host=0.0.0.0"]
