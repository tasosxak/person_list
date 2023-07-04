# pull the python image
FROM python:3.8-alpine

# copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies described in the requirements file
RUN pip install -r requirements.txt

# copy the flask files to the container
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT ["python"]
CMD ["view.py"]
