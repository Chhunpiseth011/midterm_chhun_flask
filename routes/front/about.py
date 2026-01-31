from app import app,render_template

@app.get('/about')
def about():
    return render_template('frontend/pages/about.html')