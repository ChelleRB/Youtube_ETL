# The versions below are used to specify the Airflow image as the base image
ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

#environment variable to specify the Airflow home directory
ENV AIRFLOW_HOME=/opt/airflow 

COPY requirements.txt /

RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
