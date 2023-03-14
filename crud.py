import os
import time
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError
from fastapi import HTTPException
import models, schemas
from config import Config
from database import database
from my_simple_log import log_this


def refresh_corrupted_db():
    try:
        db_name = Config.SQLITE_PATH
        if not os.path.exists(db_name):
            log_this(f"There is no db {db_name}")
        else:
            database.close()
            if recreate_db(db_name):
                database.open()
                log_this("Corrupted sqlite refreshed OK")
                return True
            else:
                log_this("Corrupted sqlite problem!")
    except Exception as e:
        log_this(f"Could not refresh corrupted db: {e}")
    return False


def recreate_db(db_name: str):
    try_count = 0
    while try_count < 3:
        try:
            if os.path.exists(db_name):
                os.remove(db_name)
            models.Base.metadata.create_all(bind=database.engine)
            return True
        except Exception as e:
            try_count += 1
            problem = f"Recreating db, attempt: {try_count}"
            log_this(problem)
            time.sleep(0.1)
    return False


def get_all_mechas(db: Session):
    try:
        return db.query(models.Mecha).all()
    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"get_all_mechas {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="get_all_mechas: Database error.")


def get_owned_mechas(db: Session, wallet: str):
    try:
        result = db.query(models.Mecha.mecha_id).filter(models.Mecha.owner == wallet).all()
        return [r[0] for r in result]

    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"get_owned_mechas {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="get_owned_mechas: Database error.")


def get_mecha(db: Session, mecha_id: int):
    try:
        return db.query(models.Mecha).filter(models.Mecha.mecha_id == mecha_id).first()
    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"get_mecha {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="get_mecha: Database error.")
        return False


def create_mecha(db: Session, mecha: schemas.Mecha):
    try:
        db_mecha = models.Mecha(
            mecha_id=mecha.mecha_id,
            owner=mecha.owner,
            staked=mecha.staked,
        )
        db.add(db_mecha)
        db.commit()
        db.refresh(db_mecha)
        return db_mecha
    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"create_mecha {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="create_mecha: Database error.")


def update_mecha_owner(db: Session, mecha_id: int, new_owner: str):
    try:
        db.query(models.Mecha).filter(models.Mecha.mecha_id == mecha_id).update({"owner": new_owner})
        db.commit()
        return db.query(models.Mecha).filter(models.Mecha.mecha_id == mecha_id).first()
    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"update_mecha_owner {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="update_mecha_owner: Database error.")


def update_mecha_staked(db: Session, mecha_id: int, staked: bool):
    try:
        db.query(models.Mecha).filter(models.Mecha.mecha_id == mecha_id).update({"staked": staked})
        db.commit()
        return db.query(models.Mecha).filter(models.Mecha.mecha_id == mecha_id).first()
    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"update_mecha_staked {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="update_mecha_staked: Database error.")


# read_task
def read_task(db: Session, task_id: int):
    try:
        return db.query(models.Task).filter(models.Task.task_id == task_id).first()
    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"read_task {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="read_task: Database error.")
        return False

# update_task
def update_task(db: Session, task_id: int, is_running: bool):
    try:
        db.query(models.Task).filter(models.Task.task_id == task_id).update({"is_running": is_running})
        db.commit()
        return db.query(models.Task).filter(models.Task.task_id == task_id).first()
    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"update_task {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="update_task: Database error.")


# create_task
def create_task(db: Session, task: schemas.Task):
    try:
        db_task = models.Task(
            task_id=task.task_id,
            is_running=task.is_running,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except (OperationalError, SQLAlchemyError, DatabaseError, ProgrammingError) as e:
        db.rollback()
        log_this(f"create_task {e}")
        if not refresh_corrupted_db():
            raise HTTPException(status_code=500, detail="create_task: Database error.")

