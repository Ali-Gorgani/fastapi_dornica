# ------------------------- Libraries -------------------------

from fastapi import Depends, APIRouter, HTTPException, Response
from sqlalchemy.orm import Session
from starlette import status

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user_with_scope

# ------------------------- Implement Users with SQLALCHEMY -------------------------
router = APIRouter(
    prefix="/listings",
    tags=['Listings']
)


@router.get('/{id}', response_model=schemas.ListingOut)
def get_listing(id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return listing


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ListingOut)
def create_listing(post: schemas.ListingCreate, db: Session = Depends(get_db),
                   current_user: schemas.UserOut = Depends(
                       get_current_user_with_scope(required_scopes=["create:items"]))):
    new_listing = models.Listing(ownerId=current_user.id, **post.model_dump())
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(id: int, db: Session = Depends(get_db),
                   current_user: schemas.UserOut = Depends(
                       get_current_user_with_scope(required_scopes=["delete:items"]))):
    listing_query = db.query(models.Listing).filter(models.Listing.id == id)
    listing = listing_query.first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if listing.ownerId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    listing_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.ListingOut)
def update_listing(id: int, updated_post: schemas.ListingCreate, db: Session = Depends(get_db),
                   current_user: schemas.UserOut = Depends(
                       get_current_user_with_scope(required_scopes=["update:items"]))):
    listing_query = db.query(models.Listing).filter(models.Listing.id == id)
    listing = listing_query.first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    if listing.ownerId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    listing_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(listing)
    return listing
