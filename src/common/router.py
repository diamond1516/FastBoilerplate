from datetime import date, datetime

from fastapi import APIRouter, Form, UploadFile, File
from fastapi_pagination import Page, paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.deps import Database
from . import models, schemas

router = APIRouter(
    prefix="/common",
    tags=["common"],
)


@router.get("/")
async def root(db: Database):
    return {"Hello": "World"}


@router.post(
    "/products",
    response_model=schemas.ProductSchema
)
async def create_product(
        db: Database,
        name: str = Form(...),
        price: float = Form(...),
        image: UploadFile = File(...),
):
    product = models.Product(name=name, price=price, image=image)
    db.add(product)
    await db.commit()

    return product


@router.get(
    "/products",
    response_model=Page[schemas.ProductSchema]
)
async def list_products(
        db: Database,
):
    query = select(models.Product)
    return await paginate(db, query)


@router.post(
    '/users',
    response_model=schemas.UserResSchema
)
async def create_user(
        db: Database,
        data: schemas.UserCreateSchema,
):
    user = models.User(**data.model_dump())
    await db.flush(user)
    for price in range(5):
        order = models.Order(total_price=price * 1000, user=user)
        db.add(order)
    db.add(user)
    await db.commit()
    return user


@router.get(
    '/users',
    response_model=Page[schemas.UserWithOrderSchema]
)
async def list_users(db: Database):
    today = date.today()
    query = (
        select(models.User)
        .join(models.Order)
        .where(models.Order.order_date >= today)
        .options(selectinload(models.User.orders))
    )
    return await paginate(db, query)

now = datetime.now()
