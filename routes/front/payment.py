from app import app,render_template

@app.get('/payment')
def payment():
    return render_template('pageFront/payment.html')