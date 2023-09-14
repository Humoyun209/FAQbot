from datetime import datetime
from sqlalchemy import select, insert, update

from database import Statement, Session


class BaseManager:
    @classmethod
    def insert_data(cls, model, **kwargs):
        with Session() as session:
            query = insert(model).values(**kwargs).returning(model)
            row = session.execute(query)
            session.commit()
            return dir(row)

    @classmethod
    def select_data(cls, model, **filter_data):
        with Session() as session:
            query = select(model).filter_by(**filter_data)
            data = session.execute(query)
            return data.scalars().all()

    @classmethod
    def update_data(cls, model, **data):
        with Session() as session:
            query = update(model).values(**data)
            data = session.execute(query)
            session.commit()
            return True


class StatementManager:
    @classmethod
    def get_last_statements(cls):
        with Session() as session:
            current_time = datetime.now()
            yesterday = current_time.replace(current_time.day - 1)
            query = select(Statement).where(Statement.created > yesterday)
            answer = session.execute(query)
            return answer.scalars().all()
        
    @classmethod
    def update_one_data(cls, **filters):
        with Session() as session:
            query = update(Statement).values(is_new=False).filter_by(is_new=True, **filters)
            session.execute(query)
            session.commit()
            return True