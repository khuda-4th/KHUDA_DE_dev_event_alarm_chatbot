FROM apache/airflow:2.7.0-python3.8
COPY ./requirements.txt /opt/airflow/requirements.txt
WORKDIR /opt/airflow
RUN pip install -r requirements.txt && \
  export AIRFLOW_HOME=/opt/airflow 
  

