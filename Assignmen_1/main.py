from fastapi import FastAPI,Query
app = FastAPI()
@app.get("/")
def home():
    return {"message":"Welcome to our app"}

from fastapi import FastAPI

 
app = FastAPI()

 

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

    in_stock:  bool = Query(None, description='True = in stock only')

):

    result = products          # start with all products

 

    if category:

        result = [p for p in result if p['category'] == category]

 

    if max_price:

        result = [p for p in result if p['price'] <= max_price]

 

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


# ── Endpoint 7 — Return one product by its ID ──────────────────

@app.get('/products/{product_id}')

def get_product(product_id: int):

    for product in products:

        if product['id'] == product_id:

            return {'product': product}

    return {'error': 'Product not found'}


