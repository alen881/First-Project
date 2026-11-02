from fastapi import FastAPI
from models import Product

app = FastAPI()




products = [
    Product(id=1, name="Product 1", description="Trimmer", price=4.0, quantity=6),
    Product(id=2, name="Product 2", description="Blade", price=8.0, quantity=9),
    Product(id=3, name="Product 3", description="Shaver", price=12.0, quantity=12)

]

    


### Get all products

@app.get("/products")



def get_products():
    return products



## Get a specific product by ID

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}    


### Create a new product

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return products

## Update an existing product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for index in range(len(products)):
        if products[index].id == product_id:
            products[index] = updated_product
            return updated_product,"Added Succesfully"
    return {"error": "Product not found"}

## Delete a product by ID

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index in range(len(products)):
        if products[index].id == product_id:
            deleted_product = products.pop(index)
            return {"message":"Done","deleted_product": deleted_product}
    return {"error": "Product not found"}