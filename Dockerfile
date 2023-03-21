FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./ /code

EXPOSE 80

CMD ["gunicorn", "main:application", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]

# Dev
# CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "80"]