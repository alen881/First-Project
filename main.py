from fastapi import FastAPI, Depends
from models import Product
from database import session,engine
from sqlalchemy.orm import Session
import database_models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

## We should do this as react uses port 3000 and fastapi uses 8000. So we need to allow cross origin requests from react to fastapi. This is done using CORS middleware.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)

## Create the database tables
database_models.base.metadata.create_all(bind=engine)


products = [
    Product(id=1, name="Product 1", description="Trimmer", price=4.0, quantity=6),
    Product(id=2, name="Product 2", description="Blade", price=8.0, quantity=9),
    Product(id=3, name="Product 3", description="Shaver", price=12.0, quantity=12)

]

## Do this so we dont need to type session everytime we want to use the database. This is a generator function that will yield a database session and close it after use.
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

## Initializing the first data set.
def init_db():
    db= session()

##1. db.query(database_models.Product)
##This acts like the FROM products part of a SQL query.
##It tells SQLAlchemy: "Prepare a query that looks inside the table mapped to the Product class.
## Thus everytime code is run same data is not added again and again. It checks if the data is already present or not.

    count = db.query(database_models.Product).count()

    if count==0:
      for i in products:
        ## Add the product to the database 
        ## Double asterick used to convert "name"="ALen" to name="Alen" for Product to add otherwise error.
        ## We cannot use Product(**i) because Product is a Pydantic model and not a SQLAlchemy model. We need to convert it to a dictionary first using model_dump() method.
        ## We can only use the alchemy product model which is database_models.Product()
        db.add(database_models.Product(**i.model_dump()))
      db.commit()

init_db()    


### Get all products

@app.get("/products")

## Injecting dependencies

def get_products(db : Session = Depends(get_db)):
    return db.query(database_models.Product).all()



## Get a specific product by ID

@app.get("/products/{product_id}")
def get_product(product_id: int, db : Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if product:
        return product
    return {"error": "Product not found"}     


### Create a new product

@app.post("/products")

def create_product(product: Product, db : Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


## Update an existing product
## product is the variable that fetches the data row. changing prduct values , sqlalchemy will recognize that change and automatically changes it in the database usiing update statement

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product, db : Session = Depends(get_db)):
    prod = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if prod:
        prod.name = updated_product.name
        prod.description = updated_product.description
        prod.price = updated_product.price
        prod.quantity = updated_product.quantity
        db.commit()
        return "Succesfully added"
    else:
        return {"error": "Product not found"}

## Delete a product by ID

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db : Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    else:
        return {"error": "Product not found"}
    return {"error": "Product not found"}   