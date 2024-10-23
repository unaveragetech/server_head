import os
import sys
import threading
import logging
from flask import Flask, request, jsonify, send_from_directory, render_template_string, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess

# Function to check and install Flask and Flask-Login
def install_flask():
    try:
        import flask
        import flask_login
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask", "Flask-Login"])

# Set up Flask app and Login manager
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key
login_manager = LoginManager()
login_manager.init_app(app)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, username, password_hash, role, instance_name):
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.instance_name = instance_name

# In-memory user storage (for demo purposes)
users = {
    'admin': User('admin', generate_password_hash('admin_password'), 'admin', 'admin_instance'),
    'superuser': User('superuser', generate_password_hash('superuser_password'), 'superuser', 'superuser_instance'),
    'user': User('user', generate_password_hash('user_password'), 'user', 'user_instance'),
}  # Example users with roles and instance names

@login_manager.user_loader
def load_user(username):
    return users.get(username)

# Create a logger for server interactions
def setup_logger(server_id):
    logger = logging.getLogger(f'Server_{server_id}')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(f'server_{server_id}.log')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logger.addHandler(handler)
    return logger

class SimpleFlaskServer:
    def __init__(self, port, server_id):
        self.port = port
        self.server_id = server_id
        self.app = Flask(__name__)
        self.logger = setup_logger(server_id)
        self.html_dir = f"server_{server_id}/html_files"
        os.makedirs(self.html_dir, exist_ok=True)

        @self.app.route('/<path:filename>', methods=['GET'])
        def serve_file(filename):
            self.logger.info(f"Serving file: {filename}")
            return send_from_directory(self.html_dir, filename)

        @self.app.route('/files', methods=['POST'])
        @login_required
        def upload_file():
            user = load_user(session['user_id'])
            if user.role not in ['admin', 'superuser']:
                return jsonify({"error": "Access denied"}), 403
            if 'file' not in request.files:
                return jsonify({"error": "No file part"}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            filepath = os.path.join(self.html_dir, file.filename)
            file.save(filepath)
            self.logger.info(f"Uploaded file: {file.filename}")
            return jsonify({"message": "File uploaded", "filename": file.filename}), 201

        @self.app.route('/status', methods=['GET'])
        @login_required
        def health_check():
            self.logger.info("Health check called")
            return jsonify({"status": "running", "server_id": self.server_id}), 200

        @self.app.route('/restart', methods=['POST'])
        @login_required
        def restart_server():
            user = load_user(session['user_id'])
            if user.role != 'superuser':
                return jsonify({"error": "Access denied"}), 403
            self.logger.info("Restarting server")
            # Placeholder for actual restart logic
            return jsonify({"message": "Server restart initiated"}), 200

        @self.app.route('/admin')
        @login_required
        def admin():
            admin_panel = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Admin Panel</title>
            </head>
            <body>
                <h2>Admin Panel for Server {{ server_id }}</h2>
                <form action="/files" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit">Upload File</button>
                </form>
                <h3>Server Status</h3>
                <button onclick="fetch('/status').then(response => response.json()).then(data => alert(JSON.stringify(data)))">Check Status</button>
                <button onclick="fetch('/restart', { method: 'POST' }).then(response => response.json()).then(data => alert(JSON.stringify(data)))">Restart Server</button>
                <a href="/logout">Logout</a>
            </body>
            </html>
            """
            return render_template_string(admin_panel, server_id=self.server_id)

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            login_form = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Login</title>
            </head>
            <body>
                <h2>Login</h2>
                <form method="post">
                    <input type="text" name="username" placeholder="Username" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Login</button>
                </form>
            </body>
            </html>
            """
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                user = load_user(username)
                if user and check_password_hash(user.password_hash, password):
                    login_user(user)
                    return redirect(url_for('admin'))
                return 'Invalid username or password', 401
            return render_template_string(login_form)

        @self.app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect(url_for('login'))

    def run(self):
        self.logger.info(f"Starting server on port {self.port}")
        self.app.run(host='0.0.0.0', port=self.port)

def start_server(port, server_id):
    server = SimpleFlaskServer(port, server_id)
    server.run()

def main():
    install_flask()

    num_servers = int(input("Enter the number of servers to create: "))
    threads = []
    
    for server_id in range(1, num_servers + 1):
        port = 5000 + server_id  # Assign unique ports
        os.makedirs(f"server_{server_id}", exist_ok=True)  # Create directory for each server
        thread = threading.Thread(target=start_server, args=(port, server_id))
        thread.start()
        threads.append(thread)
        print(f"Server {server_id} running on http://localhost:{port}")

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
