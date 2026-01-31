import os
from fileinput import filename
from app import app,db
from flask import request, redirect,render_template, url_for,abort
from model.category import getAllCategories
from model.product import Product,getProductById,getAllProductlist
from upload_service import save_image


@app.get('/admin/product')
def products():
    module = 'product'
    rows = getAllProductlist()
    return render_template(
        'admin/Product/index.html',
                           module=module,
                           products=rows
    )

@app.get('/admin/product/form')
def form_product():
    module = 'product'
    action = request.args.get('action','add')
    if action not in ['add','edit']:
        return abort(404)

    pro_id = request.args.get('pro_id', 0)
    status = 'add' if action == 'add' else 'edit'
    product = None
    if status == 'edit':
        product = getProductById(pro_id)

    return render_template(
        'admin/Product/form.html',
        module=module,
        status=status,
        pro_id=pro_id,
        product=product,
        category=getAllCategories()

    )

@app.get('/admin/product/confirm')
def confirm_product():
    module = 'product'
    pro_id = int(request.args.get('pro_id'))
    product = Product.query.get(pro_id)
    if not product:
        return 'no product found!'
    return render_template(
        'admin/Product/confirm.html',
        module=module,
        product=product
    )

@app.post('/admin/product/delete')
def delete_product():
    module = 'product'
    pro_id = int(request.form.get('pro_id'))
    delete_image = request.form.get('delete_image')
    product = Product.query.get(pro_id)

    for fname in [delete_image, f"resized_{delete_image}", f"thumb_{delete_image}"]:
        path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
        if os.path.isfile(path):
            os.remove(path)
    if not product:
        return 'no product found!'
    else:
        db.session.delete(product)
        db.session.commit()
    back_url = redirect(url_for('products'))
    return back_url

@app.post('/admin/product/add')
def add_product():
    file = request.files['image']
    filename = None
    if file:
        images = save_image(
            file,
            app.config['UPLOAD_FOLDER'],
            app.config['ALLOWED_EXTENSIONS']
        )
        filename = images['original']

    name = request.form.get('name')
    category = request.form.get('category')
    cost = request.form.get('cost')
    price = request.form.get('price')
    description = request.form.get('description')

    product = Product(
        name=name,
        category_id=category,
        cost=cost,
        price=price,
        description=description,
        image = filename
    )
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('products'))

@app.post('/admin/product/edit')
def edit_product():
    product_id = request.form.get('product_id')
    name = request.form.get('name')
    category = request.form.get('category')
    cost = request.form.get('cost')
    price = request.form.get('price')
    description = request.form.get('description')

    product = Product.query.get(product_id)
    if not product:
        return 'no product found!'
    product.name = name
    product.category_id = category
    product.cost = cost
    product.price = price
    product.description = description
    product.image = filename

    file = request.files.get('image')
    old_image = request.form.get('old_image')

    if file and file.filename != '':
        images = save_image(
            file,
            app.config['UPLOAD_FOLDER'],
            app.config['ALLOWED_EXTENSIONS']
        )
        product.image = images['original']
        product.resized_image = images['resized']
        product.thumbnail_image = images['thumbnail']

        for fname in [old_image, f"resized_{old_image}", f"thumb_{old_image}"]:
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            if os.path.isfile(path):
                os.remove(path)
    else:
        product.image = old_image
        product.resized_image = f"resized_{old_image}"
        product.thumbnail_image = f"thumb_{old_image}"
    db.session.commit()
    return redirect(url_for('products'))

