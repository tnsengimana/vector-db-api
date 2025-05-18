FROM python:3.13.3-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONFAULTHANDLER=true
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Install dependencies required for developing within docker
# RUN apt-get update

# Install package manager globally
RUN pip install -U uv

# Create working dir
RUN mkdir /code
COPY . /code
WORKDIR /code

# Install dependencies
RUN uv sync

