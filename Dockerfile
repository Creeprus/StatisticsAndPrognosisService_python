FROM python:3.11

WORKDIR /statistic_service_python
RUN pip install --upgrade pip
COPY packages.txt .
RUN pip install --upgrade pip && pip install -r packages.txt
COPY . .
# Run the application
CMD ["python","main.py"]