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
    prefix="/products",
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
@router.get('/products', response_model=List[schemas.ProductOut])
def get_business_products(db: Session = Depends(get_db),
                    curr_business: int=Depends(oauth2.get_current_business)):
    #posts = db.query(models.Post).filter(models.Post.userid == curr_user.userid).all()
    if not curr_business:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Invalid request")
    
    product_join_query = db.query(models.Product, func.count(models.Vote.productid).label("votes")).join(models.Vote, models.Vote.productid == models.Product.productid, isouter=True).group_by(models.Product.id)
    prod = product_join_query.filter(models.Product.productid == curr_business.productid).all()
    return prod
#add data to our model
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Product)
def create_products(
        post: schemas.CreateBase, 
        db: Session = Depends(get_db), 
        curr_user: int = Depends(oauth2.get_current_business)):
    post.productid = randrange(0, 20000000)
    #if curr_user:
     #   
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid request")
    
    post.businessid = curr_user.businessid
    #cursor.execute(""" INSERT INTO posts (title, content, published, postid)
     #                   values (%s, %s, %s, %s) RETURNING * """, (post.title, 
      #                  post.content, post.published, postid))
    #posts = cursor.fetchone()
    #conn.commit()
    print(curr_user.businessid) 
    post.owner = curr_user
    products = models.Product(**post.dict())
    db.add(products)
    db.commit()
    db.refresh(products)
    return products
#title str, content str, category, category

# get a specific post using the postid
@router.get("/{productid}", response_model=schemas.ProductOut)
def get_product(
    productid: int, 
    db: Session = Depends(get_db),
    curr_user : int = Depends(oauth2.get_current_business)):
    #cursor.execute(""" SELECT * from posts WHERE postid = %s """, (str(id),))
    #post = cursor.fetchone()
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request")
    #post = db.query(models.Post).filter(models.Post.postid == postid).first()
    product_join_query = db.query(models.Product, func.count(models.Vote.productid).label("votes")).join(models.Vote, models.Vote.productid == models.Product.productid, isouter=True).group_by(models.Product.id)
    prod = product_join_query.filter(models.Product.productid == productid).first()
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {postid} was not found")
    
    if prod.Product.userid != curr_user.businessid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Could not get post")
    return prod


# delete route
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db),
    curr_user: int=Depends(oauth2.get_current_business)
    ):
    #find index in array that has required ID
    #my_posts.pop
    #cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    product_query = db.query(models.Product).filter(models.Product.productid == id)
    if product_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} does not exist")
    
    if product_query.first().userid != curr_user.devid:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                           detail="Not authorized to perform action")

    product_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update route
@router.put('/{productid}', response_model=schemas.ProductUpdate)
def update_post(
    productid: int, 
    prod:schemas.UpdateBase, 
    db: Session = Depends(get_db),
    curr_user: int= Depends(oauth2.get_current_business)
    ):
    #cursor.execute(""" UPDATE posts SET title=%s, content = %s, published = %s WHERE postid=%s RETURNING *""", 
     #               (post.title, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()vb
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid request")
    product_query = db.query(models.Product).filter(models.Product.productid == productid)
    if product_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {productid} does not exist")
    
    if product_query.first().userid != curr_user.businessid:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                           detail="Not authorized to perform action")

    product_query.update(prod.dict(), synchronize_session=False)
    db.commit()
    return  product_query.first()


