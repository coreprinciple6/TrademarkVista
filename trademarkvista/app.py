import os
from flask import Flask
from flask_graphql import GraphQLView
import graphene
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, String, Text

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/trademark_db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Database Setup
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# [Rest of the model and schema code remains the same...]

# Flask App
app = Flask(__name__)

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