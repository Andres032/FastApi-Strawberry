from pydantic import BaseModel, Field

## Models


class PostList(BaseModel):
    id : str
    description : str
    video_url : str
    created_at    : str


class PostEntry(BaseModel):
    description  : str = Field(..., example="potinejj")
    video_url : str = Field(..., example="potinejj")

class CommentList(BaseModel):
   id_comment : str
   description : str
   created_at    : str
   post_id : str


class CommentEntry(BaseModel):
  description  : str = Field(..., example="potinejj")
  post_id : str = Field(..., example="id de la post")


class CommentPost(BaseModel):
    post_id : str
    id_comment : str
    description : str


