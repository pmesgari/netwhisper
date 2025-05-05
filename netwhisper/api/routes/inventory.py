from fastapi import APIRouter

router = APIRouter()

@router.get("/example")
def get_example():
    return {"message": "Inventory endpoint is working"}