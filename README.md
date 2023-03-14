
# MM API

Helper API for Mecha Melters collection.
Python 3.10 was used.
Requirements are Python (3.8-3.10) and python modules from requirements.txt. Thirdweb currently can't work with 3.11.


## Requirements installation

    pip install -r requirements.txt

## Configuration

File **config.py** holds all app settings. All settings are read from  **.env** file.

## Run
    dev:
        uvicorn main:app

In production gunicorn is recommended.


## FastAPI documentation

[FastAPI Documentation](https://fastapi.tiangolo.com/)
