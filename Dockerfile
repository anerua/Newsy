FROM python:3
COPY . /app
WORKDIR /app
RUN pip install --verbose -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]