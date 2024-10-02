from datetime import datetime
from typing import Union

import sqlalchemy as sa
from fastapi import UploadFile
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.db import Base
from utils.customs import FileField, FileObject

order_product_association = sa.Table(
    'order_product_association', Base.metadata,
    sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id')),
    sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'))
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(100), nullable=False, unique=True)

    orders: Mapped[list['Order']] = relationship(back_populates='user')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    total_price: Mapped[float] = mapped_column(sa.Float, nullable=False)

    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='orders')

    products: Mapped[list['Product']] = relationship(
        secondary=order_product_association, back_populates='orders'
    )
    order_details: Mapped[list['OrderDetail']] = relationship(
        'OrderDetail', back_populates='order'
    )


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    price: Mapped[float] = mapped_column(sa.Float, nullable=False)
    image: Mapped[Union['FileObject', 'UploadFile']] = mapped_column(
        FileField(upload_to='products/'), nullable=False, unique=True
    )

    orders: Mapped[list['Order']] = relationship(
        secondary=order_product_association, back_populates='products'
    )


class OrderDetail(Base):
    __tablename__ = 'order_details'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    price: Mapped[float] = mapped_column(sa.Float, nullable=False)
    total: Mapped[float] = mapped_column(sa.Float, nullable=False)

    order_id: Mapped[int] = mapped_column(sa.ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(sa.ForeignKey('products.id'), nullable=False)

    # Munosabatlar
    order: Mapped['Order'] = relationship(back_populates='order_details')
    product: Mapped['Product'] = relationship()


