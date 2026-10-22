from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'secret123'

# Simple HTML Template
HTML = """
<!DOCTYPE html>
<html>
<head><title>Vulnerable App</title></head>
<body>
    <h2>Vulnerable Login Page</h2>
    <p>Try SQLi: ' OR '1'='1</p>
    {% if not session.get('logged_in') %}
    <form method="POST">
        Username: <input name="username"><br><br>
        Password: <input name="password" type="password"><br><br>
        <input type="submit" value="Login">
    </form>
    {% else %}
    <h2>Welcome admin!</h2>
    <p>This page is vulnerable to XSS. Try: &lt;script&gt;alert('XSS')&lt;/script&gt;</p>
    <form method="GET">
        Search: <input name="q" value="{{ request.args.get('q','') }}">
        <input type="submit" value="Search">
    </form>
    {% if q %}
    <p>Result for: {{ q | safe }}</p>
    {% endif %}
    <br><a href="/logout">Logout</a>
    {% endif %}
    
    {% if message %}
    <p style="color:red">{{ message }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    q = request.args.get('q', '')
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABLE SQL Query simulation
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        print(query) # This will show in black window
        
        # Vulnerable check - SQLi bypass
        if "' OR '1'='1" in username or "admin" in username:
            session['logged_in'] = True
            return redirect(url_for('login', q=q))
        elif username == "admin" and password == "admin123":
            session['logged_in'] = True
            return redirect(url_for('login'))
        else:
            message = "Login Failed!"
            
    return render_template_string(HTML, message=message, q=q)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)