from functools import wraps
from typing import Any

from fastapi import HTTPException
from sqlalchemy import cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_
from starlette import status


class ObjectManager:
    excluded_fields = ['session', 'commit']

    @staticmethod
    def validate_fields(func):
        @wraps(func)
        async def wrapper(cls, **kwargs):
            for field_name in kwargs.keys():
                if field_name in cls.excluded_fields:
                    continue
                if not hasattr(cls, field_name):
                    raise ValueError(f"{field_name} is not a valid field of {cls.__name__}")
            return await func(cls, **kwargs)

        return wrapper

    @classmethod
    @validate_fields
    async def create(cls, *, session: AsyncSession, commit: bool = True, **kwargs):
        instance = cls(**kwargs)
        session.add(instance)
        if commit:
            await session.commit()
        else:
            await session.flush()
        await session.refresh(instance)
        return instance

    async def update(self, *, session: AsyncSession, commit: bool = True) -> None:
        await session.merge(self)
        if commit:
            await session.commit()
        else:
            await session.flush()

    async def delete(self, *, session: AsyncSession, commit: bool = True) -> None:
        await session.delete(self)
        if commit:
            await session.commit()
        else:
            await session.flush()

    @classmethod
    async def get(cls, *, session, relationships: list[str] = None, fields: list = None, **filters):
        if fields is None:
            query = select(cls)
        else:
            query = select(*fields)

        if filters:
            conditions = cls.build_filter_conditions(filters)
            query = query.where(and_(*conditions))

        if relationships:
            options = [selectinload(getattr(cls, rel)) for rel in relationships]
            query = query.options(*options)

        result = await session.execute(query)

        if fields:
            if len(fields) == 1:
                objs = result.scalars().one()
            else:
                objs = result.fetchone()
        else:
            objs = result.scalar_one_or_none()
        return objs

    @classmethod
    async def get_or_404(cls, *, session, **kwargs):
        obj = await cls.get(session=session, **kwargs)
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{cls.__name__} not found")
        return obj

    @classmethod
    def build_filter_conditions(cls, filters: dict) -> list:
        conditions = []
        for key, value in filters.items():
            if '__' in key:
                field, operator = key.split('__', 1)
                column = getattr(cls, field)
                if operator == 'gt':
                    conditions.append(column > value)
                elif operator == 'gte':
                    conditions.append(column >= value)
                elif operator == 'lt':
                    conditions.append(column <= value)
                elif operator == 'lte':
                    conditions.append(column <= value)
                elif operator == 'ne':
                    conditions.append(column != value)
                elif operator == 'in':
                    conditions.append(column.in_(value))
                elif operator == 'contains':
                    conditions.append(column.contains(value))
                elif operator == 'date':
                    conditions.append(cast(column, Date) == value)
                else:
                    conditions.append(column == value)
            else:
                conditions.append(getattr(cls, key) == value)
        return conditions

    @classmethod
    async def get_all(
            cls,
            *,
            session: AsyncSession,
            relationships: list[str] = None,
            limit: int = None,
            offset: int = None,
            order_by: tuple[Any] = None,
            annotate: dict = None,
            fields: list = None,
            count_only: bool = False,
            **filters
    ):
        relationships = relationships or []
        fields = fields or []

        query = select(func.count()) if count_only else select(cls) if not fields else select(*fields)

        if filters:
            conditions = cls.build_filter_conditions(filters)
            query = query.where(and_(*conditions))

        if relationships:
            options = [selectinload(getattr(cls, rel)) for rel in relationships]
            query = query.options(*options)
        if annotate:
            for alias, expr in annotate.items():
                query = query.add_columns(expr.label(alias))
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if order_by is not None:
            query = query.order_by(*order_by)

        result = await session.execute(query)

        if count_only:
            return result.scalar()
        elif fields:
            if len(fields) == 1:
                objs = result.scalars().all()
            else:
                objs = result.fetchall()
        elif annotate:
            objs = result.all()
        else:
            objs = result.scalars().all()

        return objs


__all__ = ["ObjectManager"]
