import os
from flask import Flask
from flask_graphql import GraphQLView
import graphene
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, String, Text

# Flask App
app = Flask(__name__)

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Database Setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# SQLAlchemy Model
class TrademarkModel(Base):
    __tablename__ = 'trademarks'
    id = Column(Integer, primary_key=True)
    category_code = Column(String)
    mark_identification = Column(Text)
    serial_number = Column(String, unique=True)
    case_file_owners = Column(Text)
    status = Column(String)
    xml_filename = Column(String)

# GraphQL Schema
class Trademark(graphene.ObjectType):
    id = graphene.Int()
    category_code = graphene.String()
    mark_identification = graphene.String()
    serial_number = graphene.String()
    case_file_owners = graphene.String()
    status = graphene.String()
    xml_filename = graphene.String()

class Query(graphene.ObjectType):
    all_trademarks = graphene.List(Trademark)
    trademark_by_serial = graphene.Field(Trademark, serial_number=graphene.String())
    trademarks_by_category = graphene.List(Trademark, category_code=graphene.String())
    search_marks = graphene.List(Trademark, keyword=graphene.String())

    def resolve_all_trademarks(self, info):
        with Session(engine) as session:
            return session.execute(select(TrademarkModel)).scalars().all()

    def resolve_trademark_by_serial(self, info, serial_number):
        with Session(engine) as session:
            return session.execute(
                select(TrademarkModel).filter_by(serial_number=serial_number)
            ).scalar_one_or_none()

    def resolve_trademarks_by_category(self, info, category_code):
        with Session(engine) as session:
            return session.execute(
                select(TrademarkModel).filter_by(category_code=category_code)
            ).scalars().all()

    def resolve_search_marks(self, info, keyword):
        with Session(engine) as session:
            return session.execute(
                select(TrademarkModel).filter(
                    TrademarkModel.mark_identification.ilike(f'%{keyword}%')
                )
            ).scalars().all()

schema = graphene.Schema(query=Query)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))