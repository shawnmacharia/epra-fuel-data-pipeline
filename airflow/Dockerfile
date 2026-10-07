FROM apache/airflow:2.10.5

USER airflow

ARG AIRFLOW_VERSION=2.10.5
ARG PYTHON_VERSION=3.12

COPY requirements-airflow.txt /tmp/requirements-airflow.txt
COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir \
	--constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt" \
	-r /tmp/requirements-airflow.txt