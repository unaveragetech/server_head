import os
import json
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this for production
login_manager = LoginManager()
login_manager.init_app(app)

# Directories
USER_DATA_FILE = 'user_data.json'
INSTANCE_DIR = 'instances'
os.makedirs(INSTANCE_DIR, exist_ok=True)

# Load user data
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump({}, f)

with open(USER_DATA_FILE, 'r') as f:
    users = json.load(f)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = users[username]['role']  # Get user role

@login_manager.user_loader
def load_user(user_id):
    return User(user_id) if user_id in users else None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        instance_name = request.form['instance_name']
        role = request.form['role']

        if username in users:
            flash('Username already exists!', 'danger')
        elif instance_name in os.listdir(INSTANCE_DIR):
            flash('Instance name already taken!', 'danger')
        else:
            users[username] = {
                'password': generate_password_hash(password),
                'instance_name': instance_name,
                'role': role  # Store user role
            }
            os.makedirs(os.path.join(INSTANCE_DIR, instance_name), exist_ok=True)
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(users, f)
            flash('Registration successful! You can log in now.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/instances')
@login_required
def manage_instances():
    instance_name = users[current_user.id]['instance_name']
    instances = os.listdir(INSTANCE_DIR)
    return render_template('instances.html', instances=instances, user_instance=instance_name)

@app.route('/delete_instance/<instance_name>')
@login_required
def delete_instance(instance_name):
    if users[current_user.id]['instance_name'] == instance_name:
        instance_path = os.path.join(INSTANCE_DIR, instance_name)
        if os.path.exists(instance_path):
            os.rmdir(instance_path)  # Use shutil.rmtree for non-empty directories
            flash(f'Instance {instance_name} deleted!', 'success')
            del users[current_user.id]
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(users, f)
        else:
            flash('Instance not found', 'danger')
    else:
        flash('You do not have permission to delete this instance', 'danger')
    return redirect(url_for('manage_instances'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
