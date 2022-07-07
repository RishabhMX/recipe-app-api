# Install Python 3.9 image
FROM python:3.9-alpine3.13

 # maintainer of the image
LABEL maintainer="teki9"

 # for faster response
ENV PYTHONBUFFERED 1


COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#to create script file for helper scripts
COPY ./scripts /scripts
COPY ./app /app
WORKDIR /app
EXPOSE 8000

#getting overrided in decker-compose.yml
ARG DEV=false
# &&/  used to create new lines for lighter dockerfile
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
#will be on docker image after its built
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    #to install
    #linux header for wsgi server installation
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    #if condition in shell scripting
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    # fi means end of if condition
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    #creating media and static folders
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    #giving ownership of folders to user
    chown -R django-user:django-user /vol/ && \
    chmod -R 755 /vol/web && \
    #to make script directory executable
    chmod -R +x /scripts


ENV PATH="/scripts:/py/bin:$PATH"

USER django-user

#script to run application
CMD ["run.sh"]


