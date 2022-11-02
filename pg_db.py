import databases, sqlalchemy
from sqlalchemy import Column, String, ForeignKey

 

## Postgres Database
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/backend"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

posts = sqlalchemy.Table(
    "post",
    metadata,
   
    sqlalchemy.Column("id"        , sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("description"  , sqlalchemy.String),
    sqlalchemy.Column("video_url"  , sqlalchemy.String),
    sqlalchemy.Column("created_at" , sqlalchemy.String),
)

comments = sqlalchemy.Table(
    "comment",
    metadata,
   
    Column('id_comment', String, primary_key=True),
    Column('description', String(255)),
    Column('created_at', String), 
    Column('post_id', String, ForeignKey("post.id"), nullable=False))
    
#)

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
metadata.create_all(engine)