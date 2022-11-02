import model as mdComment
import datetime, uuid
import model as mdPost
import model as mdCommentPost
from pg_db import database, posts, comments
from fastapi import FastAPI
from straw import Query, Mutation
from strawberry.asgi import GraphQL
import strawberry
from typing import List


#http://127.0.0.1:8000/api/v2/docs Probar la api con fast
#Probar la api integrada con strawberry http://127.0.0.1:8000/graphql

app = FastAPI(
    docs_url="/api/v2/docs",
    title="PostComennts",
   
    
)


schema = strawberry.Schema(Query,Mutation)
graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

    

@app.get("/posts", response_model=List[mdPost.PostList], tags=["Posts"])
async def find_all_post():
    query = posts.select()
    return await database.fetch_all(query)

@app.get("/posts/{postId}", response_model=mdPost.PostList, tags=["Posts"])
async def find_post_by_id(posId: str):
    query = posts.select().where(posts.c.id == posId)
    return await database.fetch_one(query)

@app.post("/posts", response_model=mdPost.PostList, tags=["Posts"])
async def createpost(pos: mdPost.PostEntry):
    gID   = str(uuid.uuid1())
    gDate =str(datetime.datetime.now())
    query = posts.insert().values(
        id = gID,
        description   = pos.description,
        video_url = pos.video_url,
        created_at  = gDate,
        
    ) 

    await database.execute(query)
    return {
        "id": gID,
        **pos.dict(),
        "created_at":gDate,
        
    }


## Tabla Comments


@app.get("/comments", response_model=List[mdComment.CommentList], tags=["Comments"])
async def find_all_comment():
    query = comments.select()
    return await database.fetch_all(query)

@app.get("/comments/{comenId}", response_model=mdComment.CommentList, tags=["Comments"])
async def find_comment_by_id(comenId: str):
    query = comments.select().where(comments.c.id_comment == comenId)
    return await database.fetch_one(query)

@app.get("/commentsPost/{PostId}",response_model=mdCommentPost.CommentPost, tags=["Comments of Post"])
async def get_comments_by_post_id(PostId: str):
     query = comments.select().where(comments.c.post_id == PostId)
     return await database.fetch_one(query)

@app.post("/comments", response_model=mdComment.CommentList, tags=["Comments"])
async def createcomment(comen: mdComment.CommentEntry):
    gID1   = str(uuid.uuid1())
    gDate1 =str(datetime.datetime.now())
    query = comments.insert().values(
        id_comment= gID1,
        description   = comen.description,
        created_at  = gDate1,
        post_id = comen.post_id
        
    ) 

    await database.execute(query)
    return {
        "id_comment": gID1,
        **comen.dict(),
        "created_at":gDate1,
        
    }
    
