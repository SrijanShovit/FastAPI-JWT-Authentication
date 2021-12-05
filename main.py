import uvicorn
from fastapi import FastAPI,Body,Depends
from app.model import PostSchema,UserSchema,UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id": 1,
        "title": "Penguins",
        "content": "Penguins"
    },
    {
        "id": 2,
        "title": "Tigers",
        "content": "Tigers"
    },
    {
        "id": 3,
        "title": "Koalas",
        "content": "Koalas"
    },
]

users = []

app = FastAPI()
#1 Get - for testing
@app.get('/',tags=["test"])
def greet():
    return {"Hello World"}


#2 Get Posts
@app.get("/posts",tags=["posts"])
def get_posts():
    return {"data" : posts}

#3 Get Single Posts by {id}
@app.get("/posts/{id}",tags =["posts"])
def get_one_post(id:int):
    if id>len(posts):
        return {
            "error":"Post with this ID does not exist!"
        }
    for post in posts:
        if post["id"] == id:
            return {
                "data":post
            }


#4 Post a blog post [A handler for creating a post]
#dependencies is used to restrict that only validated users can post

@app.post("/posts",dependencies=[Depends(jwtBearer())],tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info" : "Post added"
    }
    

#5 User Signup [Create a new user]
@app.post("/user/signup",tags=["user"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user_exists(data : UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False
    
@app.post("/user/login",tags=["user"])
def user_login(user : UserLoginSchema = Body(default=None)):
    if check_user_exists(user):
        return signJWT(user.email)
    else:
        return {
            "error" : "Invalid login details!"
        }
        