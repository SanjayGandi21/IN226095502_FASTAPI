from fastapi import FastAPI,Query
from pydantic import BaseModel, Field
from typing import Optional,List

app = FastAPI()

# ── Pydantic model-1 ───────────────────────────────────────────────────────────

class OrderRequest(BaseModel):

    customer_name:    str = Field(..., min_length=2, max_length=100)

    product_id:       int = Field(..., gt=0)

    quantity:         int = Field(..., gt=0, le=100)

    delivery_address: str = Field(..., min_length=10)


# ── Temporary data — acting as our database for now ──────────

products = [

    {'id': 1, 'name': 'Wireless Mouse',     'price': 499,  'category': 'Electronics', 'in_stock': True },

    {'id': 2, 'name': 'Notebook',           'price':  99,  'category': 'Stationery',  'in_stock': True },

    {'id': 3, 'name': 'USB Hub',             'price': 799, 'category': 'Electronics', 'in_stock': False},

    {'id': 4, 'name': 'Pen Set',             'price':  49, 'category': 'Stationery',  'in_stock': True },

    {'id': 5, 'name': 'Laptop Stand',        'price':  1299, 'category': 'Electronics',  'in_stock': True },

    {'id': 6, 'name': 'Mechanical Keyboard', 'price':  999, 'category': 'Electronics',  'in_stock': False },

    {'id': 7, 'name': 'Webcam',              'price':  1499, 'category': 'Electronics',  'in_stock': True },
    

]
feedback = []

orders = []

order_counter = 1

 

# ── Endpoint 0 — Home ────────────────────────────────────────

@app.get('/')

def home():

    return {'message': 'Welcome to our E-commerce API'}

 

# ── Endpoint 1 — Return all products ──────────────────────────

@app.get('/products')

def get_all_products():

    return {'products': products, 'total': len(products)}
@app.get('/products/filter')

def filter_products(

    category:  str  = Query(None, description='Electronics or Stationery'),

    max_price: int  = Query(None, description='Maximum price'),

    in_stock:  bool = Query(None, description='True = in stock only'),

    min_price: int = Query(None, description='Minimum price')

):

    result = products          # start with all products

 

    if category:

        result = [p for p in result if p['category'] == category]

 

    if max_price:

        result = [p for p in result if p['price'] <= max_price]
    

    if min_price:
        result = [p for p in result if p['price'] >= min_price]
 

    if in_stock is not None:

        result = [p for p in result if p['in_stock'] == in_stock]

 

    return {'filtered_products': result, 'count': len(result)}

# ── Endpoint 2 — Return products by category ──────────────────
@app.get('/products/category/{category_name}')

def get_category(category_name: str):
    
    result=[p for p in products if p["category"]==category_name]
    if not result: 
        return {"error": "No products found in this category"}
    return  {"category": category_name, "products": result, "total": len(result)}


# ── Endpoint 3 — Return products by stock ──────────────────
@app.get("/products/instock") 
def get_instock(): 
    available = [p for p in products if p["in_stock"] == True] 
    return {"in_stock_products": available, "count": len(available)}

# ── Endpoint 4 — Store summary ──────────────────

@app.get("/store/summary")
def get_summary():
    stock=[p for p in products if p['in_stock']]
    out_stock=len(products)-len(stock)
    category=list(set(p["category"] for p in products))

    return {"store_name":"My Ecommerce_Store","total_products":len(products),"in_stock":len(stock),"out_of_stock":out_stock,"categories":category}


# ── Endpoint 5 — search ──────────────────
@app.get("/products/search/{keyword}")
def get_search(keyword:str):
    product=[p for p in products if keyword.lower() in p['name'].lower()]
    if not product:
        return {"message":"No products matched your search"}
    return {"Keyword":keyword,"Matched Products":product, "Total_Products":len(product)}

# ── Endpoint 6 — Deals ──────────────────
@app.get("/products/deals")
def get_deals():
    cheap=min(products, key=lambda p: p['price'])
    expensive=max(products, key=lambda p: p['price'])
    return { "best_deal": cheap, "premium_pick": expensive}

@app.get("/products/{product_id}/price")
def get_cart(product_id:int):
    for p in products:
        if p['id']==product_id:
            return {"name":p['name'],'Price':p['price']}
    return {'message':'Add Products'}

@app.get('/products/summary')
def product_summary():
    in_stock=[p for p in products if p['in_stock']]
    out_stock=len(products)-len(in_stock)
    exp=max(products, key=lambda p: p["price"])
    cheap=min(products, key=lambda p: p["price"])
    categories=list(set(p['category'] for p in products))

    return {'Total Products':len(products),'in_stock_count':len(in_stock),'out_stock_count':out_stock,'most expensive':{'name':exp['name'],'price':exp['price']},'Cheapest':{'name':cheap['name'],'price':cheap['price']},'Categories':categories}

# ── Endpoint 7 — Return one product by its ID ──────────────────

@app.get('/products/{product_id}')

def get_product(product_id: int):

    for product in products:

        if product['id'] == product_id:

            return {'product': product}

    return {'error': 'Product not found'}

@app.post('/orders')

def place_order(order_data: OrderRequest):

    global order_counter

    product = next((p for p in products if p['id']==order_data.product_id), None)

    if product is None:          return {'error': 'Product not found'}

    if not product['in_stock']:  return {'error': f"{product['name']} is out of stock"}

    total_price = product['price'] * order_data.quantity

    order = {'order_id': order_counter, 'customer_name': order_data.customer_name,

'product': product['name'], 'quantity': order_data.quantity,

'delivery_address': order_data.delivery_address,

'total_price': total_price, 'status': 'pending'}

    orders.append(order)

    order_counter += 1

    return {'message': 'Order placed successfully', 'order': order}

 

@app.get('/orders')

def get_all_orders():

    return {'orders': orders, 'total_orders': len(orders)}

# ── Pydantic model-2 ───────────────────────────────────────────────────────────

class customer_feedback(BaseModel):

    customer_name:    str = Field(..., min_length=2, max_length=100)

    product_id:       int = Field(..., gt=0)

    rating:         int = Field(..., ge=1, le=5)

    comment: Optional[str] = Field(None, max_length=300)
    

@app.post('/feedback')
def submit_feedback(data: customer_feedback):
    feedback.append(data.model_dump())
    return {
        "message":        "Feedback submitted successfully",
        "feedback":       data.model_dump(),
        "total_feedback": len(feedback),
    }

class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity:   int = Field(..., gt=0, le=50)

class BulkOrder(BaseModel):
    company_name:  str           = Field(..., min_length=2)
    contact_email: str           = Field(..., min_length=5)
    items:         List[OrderItem] = Field(..., min_items=1)

@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed, failed, grand_total = [], [], 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal})
    return {"company": order.company_name, "confirmed": confirmed,
            "failed": failed, "grand_total": grand_total}


# In place_order — change 'confirmed' to 'pending':


# New GET by order ID:
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return {"order": order}
    return {"error": "Order not found"}

# PATCH to confirm:
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"
            return {"message": "Order confirmed", "order": order}
    return {"error": "Order not found"}
