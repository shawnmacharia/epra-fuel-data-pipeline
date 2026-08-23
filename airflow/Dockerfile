FROM apache/airflow:2.10.5

USER airflow

# Copy the requirements file from the build context (project root) into the container
COPY requirements-airflow.txt /tmp/requirements-airflow.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements-airflow.txt