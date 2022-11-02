from email.policy import HTTP
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from fastapi import ( APIRouter,
 HTTPException, Response, status, Depends)
from random import randrange
from typing import List, Optional
from sqlalchemy import func
router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#get all data from our model Posts 
@router.get("/" , response_model=List[schemas.ProductOut])
def get_posts(
    db: Session = Depends(get_db),
    limit: int=10,
    search: Optional[str] =""
):
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

    result_query = db.query(models.Product, func.count(models.Vote.productid).label("votes")).join(models.Vote, models.Vote.productid == models.Product.productid , isouter=True).group_by(models.Product.id)
    result = result_query.filter(models.Product.title.contains(search)).limit(limit).all()
    return result
    
# get all projects of collaborator 
@router.get('/products', response_model=List[schemas.PostOut])
def get_colab_posts(db: Session = Depends(get_db),
                    curr_user: int=Depends(oauth2.get_current_dev)):
    #posts = db.query(models.Post).filter(models.Post.userid == curr_user.userid).all()
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid request")
    
    post_join_query = db.query(models.Post, func.count(models.Vote.postid).label("votes")).join(models.Vote, models.Vote.postid == models.Post.postid, isouter=True).group_by(models.Post.id)
    post = post_join_query.filter(models.Post.userid == curr_user.devid).all()
    return post
#add data to our model
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
        post: schemas.CreateBase, 
        db: Session = Depends(get_db), 
        curr_user: int = Depends(oauth2.get_current_dev)):
    post.postid = randrange(0, 20000000)
    #if curr_user:
     #   
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid request")
    
    post.userid = curr_user.devid
    #cursor.execute(""" INSERT INTO posts (title, content, published, postid)
     #                   values (%s, %s, %s, %s) RETURNING * """, (post.title, 
      #                  post.content, post.published, postid))
    #posts = cursor.fetchone()
    #conn.commit()
    print(curr_user.devid) 
    posts = models.Post(**post.dict())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts
#title str, content str, category, category

# get a specific post using the postid
@router.get("/{postid}", response_model=schemas.PostOut)
def get_post(
    postid: int, 
    db: Session = Depends(get_db),
    curr_user : int = Depends(oauth2.get_current_dev)):
    #cursor.execute(""" SELECT * from posts WHERE postid = %s """, (str(id),))
    #post = cursor.fetchone()
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request")
    #post = db.query(models.Post).filter(models.Post.postid == postid).first()
    post_join_query = db.query(models.Post, func.count(models.Vote.postid).label("votes")).join(models.Vote, models.Vote.postid == models.Post.postid, isouter=True).group_by(models.Post.id)
    post = post_join_query.filter(models.Post.postid == postid).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {postid} was not found")
    
    if post.Post.userid != curr_user.devid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not get post")
    return post


# delete route
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    curr_user: int=Depends(oauth2.get_current_dev)
    ):
    #find index in array that has required ID
    #my_posts.pop
    #cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.postid == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} does not exist")
    
    if post_query.first().userid != curr_user.devid:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                           detail="Not authorized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update route
@router.put('/{postid}', response_model=schemas.PostUpdate)
def update_post(
    postid: int, 
    post:schemas.UpdateBase, 
    db: Session = Depends(get_db),
    curr_user: int= Depends(oauth2.get_current_dev)
    ):
    #cursor.execute(""" UPDATE posts SET title=%s, content = %s, published = %s WHERE postid=%s RETURNING *""", 
     #               (post.title, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()vb
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid request")
    post_query = db.query(models.Post).filter(models.Post.postid == postid)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {postid} does not exist")
    
    if post_query.first().userid != curr_user.devid:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                           detail="Not authorized to perform action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()


