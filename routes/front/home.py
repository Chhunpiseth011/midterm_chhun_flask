from app import app
from flask import render_template, request
from model.product import getAllProductlist
from model.category import getAllCategories

from model.product import Product
from model.category import Category


def normalize_products(products):
    data = []
    for p in products:
        image_url = None
        if p.get("image"):
            image_url = f"/static/uploads/{p['image']}"

        data.append({
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "description": p.get("description"),
            "image": image_url,
            "category": p.get("category")
        })
    return data

@app.get('/')
@app.get('/home',endpoint='home')
def home():
    products = getAllProductlist()
    categories = getAllCategories()

    products = normalize_products(products)

    return render_template(
        'frontend/home.html',
        products=products,
        categories=categories,
        selected_category=None
    )


@app.get('/product_detail/<int:product_id>') # Added / before <int:product_id>
def product_detail(product_id):
    # Use get_or_404 instead of get to handle missing IDs gracefully
    product = Product.query.get_or_404(product_id)
    categories = getAllCategories()

    return render_template(
        'frontend/pages/product/product_detail.html',
        product=product,
        categories=categories,
        selected_category=None
    )

@app.route('/products')
def product_list():
    # 1. Get the category_id from the URL (e.g., ?category_id=5)
    category_id = request.args.get('category_id', type=int)

    # 2. Fetch all categories for the sidebar
    categories = Category.query.all()

    # 3. Fetch products (Filtered or All)
    if category_id:
        products = Product.query.filter_by(category_id=category_id).all()
        # Optional: Get the name of the current category for the title
        active_category = Category.query.get(category_id)
        page_title = active_category.name if active_category else "Products"
    else:
        products = Product.query.all()
        page_title = "All Products"

    return render_template('frontend/pages/product/products.html',
                           products=products,
                           categories=categories,
                           current_category_id=category_id,
                           page_title=page_title)

#
# @app.get('/products')
# def products():
#     products = getAllProductlist()
#     categories = getAllCategories()
#
#     products = normalize_products(products)
#
#     return render_template(
#         'frontend/home.html',
#         products=products,
#         categories=categories,
#         selected_category=None
#     )


# @app.get("/products",endpoint="products_filter")
# def products_filter():
#     category = request.args.get('category')
#     products = getAllProductlist()
#     categories = getAllCategories()
#
#     products = normalize_products(products)
#
#     if category:
#         products = [p for p in products if p['category'] == category]
#
#     return render_template(
#         'pageFront/home.html',
#         products=products,
#         categories=categories,
#         selected_category=category
#     )
