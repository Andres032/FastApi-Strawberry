from typing import List
import uuid
import datetime
import strawberry
import typing
from pg_db import database, posts, comments



## Models

@strawberry.type
class Post:
    id : str
    description : str
    video_url : str
    created_at    : str

@strawberry.input
class PostEnt:
    description  : str
    video_url : str

@strawberry.type
class Comment:
   id_comment : str
   description : str
   created_at    : str
   post_id : str

@strawberry.input
class CommentEntr:
  description  : str 
  post_id : str 

@strawberry.type
class CommentPost:
    post_id : str
    id_comment : str
    description : str
    created_at: str


#Mostrar todos los post
async def get_posts() -> List [Post]:
    query = "SELECT * FROM post"
    rows = await database.fetch_all(query)

    return [Post(id=n.id, description=n.description, video_url=n.video_url, created_at=n.created_at) for n in rows]


#Mostrar todos los comentarios
async def get_comments() -> List [Comment]:
       query = "SELECT * FROM comment"
       rows = await database.fetch_all(query)
       return [Comment(id_comment=m.id_comment, description=m.description, created_at=m.created_at,post_id=m.post_id) for m in rows]


@strawberry.type
class Query:     
    #Mostrar todos los post 
     post: List[Post] = strawberry.field(resolver=get_posts)

      #Mostrar todos los comentarios
     comment: List[Comment] = strawberry.field(resolver=get_comments)
 
     @strawberry.field
     #Adquirir post por id
     def find_post_by_id(id: str) -> Post:
        return database.fetch_one(posts.select().where(posts.c.id == id)) 
     @strawberry.field
     #Adquirir comentario por id
     def find_comment_by_id(id: str) -> Comment:
        return database.fetch_one(comments.select().where(comments.c.id_comment == id))

     @strawberry.field
     #obtener comentarios por ID de publicación
     def find_Post_comment_by_id(id: str) -> CommentPost:
        return database.fetch_one(comments.select().where(comments.c.post_id == id))

    
@strawberry.input
class Mutation:
    ##Creacion de post
   @strawberry.mutation
   async def createpost(self, data: PostEnt) -> Post:
    gID   = str(uuid.uuid1())
    gDate =str(datetime.datetime.now())
    query = posts.insert().values(
        id = gID,
        description   = data.description,
        video_url = data.video_url,
        created_at  = gDate,
        
    ) 

    await database.execute(query)
    return {
        "id": gID,
        "des"
        "created_at":gDate,
        
    }

 ##Creacion de comentarios
   @strawberry.mutation
   async def createcomment(self, data: CommentEntr) -> Comment:
    gID1   = str(uuid.uuid1())
    gDate1 =str(datetime.datetime.now())
    query = comments.insert().values(
        id_comment = gID1,
        description   = data.description,
        created_at  = gDate1,
        post_id = data.post_id
        
    ) 

    await database.execute(query)
    return {
        "id_comment": gID1,
        "des"
        "created_at":gDate1,
        
    }

    
    



   