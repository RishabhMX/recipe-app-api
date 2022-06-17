# Install Python 3.9 image
FROM python:3.9-alpine3.13 

 # maintainer of the image
LABEL maintainer="teki9"

 # for faster response
ENV PYTHONBUFFERED 1 


COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

#getting overrided in decker-compose.yml
ARG DEV=false 
# &&/  used to create new lines for lighter dockerfile
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \    
    /py/bin/pip install -r /tmp/requirements.txt && \
    #if condition in shell scripting
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    # fi means end of if condition
    fi && \  
    rm -rf /tmp && \    
    adduser \
        --disabled-password \
        --no-create-home \
        django-user    

ENV PATH="/py/bin:$PATH"

USER django-user


