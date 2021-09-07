from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.ORM.database import Base


class BaseSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        db_model: Base = None

    @classmethod
    def get(cls, db: Session, **kwargs):
        model = db.query(cls.Config.db_model).filter_by(**kwargs).one()
        return cls.from_orm(model)

    @classmethod
    def get_or_create(cls, db: Session, _defaults: {} = None, **kwargs):
        try:
            return cls.get(db, **kwargs), False
        except NoResultFound:
            defaults = _defaults or dict()
            model = cls.Config.db_model(**defaults)
            db.add(model)
            db.commit()
            db.refresh(model)
            return cls.from_orm(model), True

    def update(self, db: Session, _updates: {}):
        new_obj = self.copy(update=_updates or {})
        new_obj.save(db)
        return new_obj

    def save(self, db: Session):
        qs = db.query(self.Config.db_model).filter(self.Config.db_model.id == self.id)
        model = qs.one_or_none() or self.Config.db_model()
        updated_columns = self._get_updated_columns()
        for attr, value in self:
            if attr in updated_columns:
                setattr(model, attr, value)

        db.add(model)
        db.commit()

    def _get_updated_columns(self):
        """Exclude relationships from model's fields"""
        column_names = set()
        for name, column in self.Config.db_model.__table__.columns.items():
            if name != 'id' and isinstance(column, Column):
                column_names.add(name)

        return column_names
