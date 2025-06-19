from fastapi import APIRouter, HTTPException
from models.creature import Creature
from service import creature as service
from .error import Duplicate, Missing


router = APIRouter(prefix = "/creature")
@router.get("")
@router.get("/")

def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")

def get_one(name) -> Creature:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=201)
@router.post("/", status_code=201)

def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("/")

def modify(name: str, creature: Creature) -> Creature:
    try:
        return service.modify(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.put("/")
def replace(creature: Creature) -> Creature:
    return service.replace(creature)

@router.delete("/{name}")
def delete(name: str):
    try:
        creature = service.get_one(name)
        return service.delete(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)