from pydantic import BaseModel


class Mecha(BaseModel):
    mecha_id: int
    owner: str
    staked: int

class Task(BaseModel):
    task_id: int
    is_running: bool