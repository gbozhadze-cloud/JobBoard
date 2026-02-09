from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional


fast = FastAPI()

class CreatePotion(BaseModel):
    name: str
    ingredients: list[str] = []
    power: int = 0
    status: str

class UpdatePotion(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[list[str]] = None
    power: Optional[int] = None
    status: Optional[str] = None
# შევქმენი რათა შემეძლოს მხოლოდ ერთი ველის განახლება

@fast.get("/")
def homedirectory():
    return {"message": "Welcome to MagicLab"}


current_potions_list = []
@fast.post("/createPotion")
def create_potion(potion: CreatePotion):
    if any(p.name == potion.name for p in current_potions_list):
        raise HTTPException(status_code=400, detail="Potion with this name already exists")
    current_potions_list.append(potion)
    return {"message": f"Potion '{potion.name}' created successfully!"}

@fast.get("/get_potions")
def get_potions():
    return {"potions": current_potions_list}

@fast.delete("/delete_potion/{potion_name}")
def delete_potion(potion_name: str):
    global current_potions_list
    current_potions_list = [p for p in current_potions_list if p.name != potion_name]
    return {"message": f"{potion_name} წაშლილია "}


@fast.patch("/patch_potion/{potion_name}")
def patch_potion(potion_name: str, updated_fields: UpdatePotion):
    for p in current_potions_list:
        if p.name == potion_name:
            if updated_fields.name is not None:
                p.name = updated_fields.name
            if updated_fields.ingredients is not None:
                p.ingredients = updated_fields.ingredients
            if updated_fields.power is not None:
                p.power = updated_fields.power
            if updated_fields.status is not None:
                p.status = updated_fields.status
            return {"message": f"{potion_name}განახლებულია"}
    return {"message": "ასეთი დასახელება არ მოიძბენა"}