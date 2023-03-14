from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import time
from database import database
import models
import crud
import schemas
from config import Config
from my_simple_log import log_this
from w3helpers import get_owner, deposits_of

from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=database.engine)

application = FastAPI(
    title=Config.TITLE,
    version=Config.VERSION,
    description=Config.DESCRIPTION,
    docs_url="/mmdocumentation",
    redoc_url=None,
    responses={
        200: {"description": "Ok"},
        202: {"description": "Signal sent"},
        403: {"description": "Forbidden"},
        404: {"description": "Not found"},
        422: {"description": "Validation problem"},
        500: {"description": "Database problem"}
    },
    openapi_url="/mmopenapi.json",
)


origins = ["*"]

application.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    try:
        db = database.sessionLocal()
        yield db
    except Exception as e:
        db.rollback()
    finally:
        try:
            db.close()
        except:
            pass


db_generator = get_db()
db = next(db_generator)


# @application.get("/")
# def hello_world():
#     return {"hello": "Mechas"}

# @application.get("/mechas", tags=["db"])
# async def get_all_mechas():
#     return crud.get_all_mechas(db)


@application.get("/mecha", response_model=schemas.Mecha, tags=["mm"])
def get_mecha(mecha_id: int):
    "get Mecha by id from the api database"
    if mecha_id > 6000 or mecha_id == 0:
        raise HTTPException(status_code=404)
    db_res = crud.get_mecha(db, mecha_id)
    if db_res:
        json = jsonable_encoder(db_res)
        return JSONResponse(json)


@application.get("/update_mecha/{mecha_id}", tags=["mm"])
async def update_mecha(mecha_id:int):
    "update db Mecha owner if the blockchain owner is different"
    
    if mecha_id > 6000 or mecha_id == 0:
        raise HTTPException(status_code=404)
    
    owner = get_owner(mecha_id)
    staked = 0
    if owner == Config.MM_STAKING_ADD:
        staked = 1
    mecha = schemas.Mecha(mecha_id=mecha_id,owner=owner,staked=staked)
    exists = crud.get_mecha(db=db, mecha_id=mecha_id)
    if not exists:
        crud.create_mecha(db=db, mecha=mecha)
    elif exists.owner != mecha.owner:
        crud.update_mecha_owner(db=db, mecha_id=mecha_id, new_owner=owner)
    elif exists.owner == mecha.owner:
        return "not changed"
    return "updated"


@application.get("/owned_mechas", tags=["mm"])
async def get_owned_mechas(wallet: str):
    "get list of owned mecha ids from the db"
    return crud.get_owned_mechas(db, wallet)

def process_all_mechas():   
    start_time = time.time()
    errors = 0
    for i in range (1,6001):
        try:
            # read contract
            owner = get_owner(i)
            # set data
            staked = 0
            if owner == Config.MM_STAKING_ADD:
                staked = 1
            mecha = schemas.Mecha(mecha_id=i,owner=owner,staked=staked)
            # get mecha
            exists = crud.get_mecha(db=db, mecha_id=i)
            # create mecha
            if not exists:
                crud.create_mecha(db=db, mecha=mecha)
            # update owner
            elif exists.owner != mecha.owner:
                crud.update_mecha_owner(db=db, mecha_id=i, new_owner=owner)
        except:
            errors +=1
    end_time = time.time()
    elapsed = end_time - start_time
    message = f"process_all_mechas, errors: {errors}, total time: {elapsed} seconds" 
    if errors > 0:
        log_this(message)
    


def periodic_task():
    while True:
        db_task = crud.read_task(db=db, task_id=1)
        json = jsonable_encoder(db_task)
        is_running = json["is_running"]
        if not is_running:
                break
        # My Cron Job
        process_all_mechas()

        # 12h sleep in seconds
        time.sleep(60*60*12)
    # end
    crud.update_task(db=db, task_id=1, is_running=False)
    return

@application.post("/start-cron", tags=["mm"], status_code=202)
async def start_cron(background_tasks: BackgroundTasks, password: str):
    "Start background task to periodically update all mechas"
    if password == "montypython":
        db_task = crud.read_task(db=db, task_id=1)
        if not db_task:
            task = schemas.Task(task_id=1,is_running=True)
            crud.create_task(db=db, task=task)
            db_task = crud.read_task(db=db, task_id=1)
        json = jsonable_encoder(db_task)
        is_running = json["is_running"]

        if not is_running:
            crud.update_task(db=db, task_id=1, is_running=True)
            background_tasks.add_task(periodic_task)
            return "started"
        return "already running"
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
        
        
@application.post("/stop-cron", tags=["mm"], status_code=202)
async def stop_cron(background_tasks: BackgroundTasks, password: str):
    "Stop periodic updating of all Mechas."
    if password == "montypython":
        db_task = crud.read_task(db=db, task_id=1)
        json = jsonable_encoder(db_task)
        is_running = json["is_running"]
        if is_running:
            crud.update_task(db=db, task_id=1, is_running=False)
            background_tasks.tasks.clear()
            return "stopped"
        return "not running"
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


# @application.get("/deposits_of",response_model=str, tags=["mm staking contract"])
# def get_deposits_of(wallet:str):
#     return deposits_of(wallet)


