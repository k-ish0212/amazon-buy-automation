#FROM python:3-alpine
FROM joyzoursky/python-chromedriver:3.9-alpine
#FROM python:3.8-alpine3.11

RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN apk add -U chromium chromium-chromedriver

# Setup project folder
ARG project_dir=/python/app/
WORKDIR ${project_dir}

# Install requirements
COPY requirements.txt requirements.txt
RUN set -x && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Copy in script
COPY . ${project_dir}

# Run baby!
CMD ["python", "main.py"]
