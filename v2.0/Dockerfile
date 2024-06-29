FROM apache/airflow:2.7.0-python3.8
USER root
COPY ./requirements.txt /opt/airflow/requirements.txt
WORKDIR /opt/airflow
RUN export AIRFLOW_HOME=/opt/airflow && \
  apt-get update && \
  apt-get install wget -y && \
  wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  apt-get install -y ./google-chrome-stable_current_amd64.deb
USER airflow
RUN pip install -r requirements.txt
