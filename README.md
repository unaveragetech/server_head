Here’s the updated README.md with your GitHub repository link and contact email included:

```markdown
# Multi-Instance Flask Web Server

This project provides a multi-instance Flask web server that allows users to serve HTML files from their local machine. The server includes a web interface for user authentication, file management, and logging. Users can upload files, check server status, and restart their server instances based on their assigned roles.
```
## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [User Roles and Permissions](#user-roles-and-permissions)
- [File Management](#file-management)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
```
## Features

- **Multi-Instance Support**: Spin up multiple Flask server instances on different ports.
- **Role-Based Access Control**: Three user roles with different permissions:
  - **User**: Can view and manage their own files.
  - **Admin**: Can upload files and check server status.
  - **Superuser**: Can restart servers and perform all admin tasks.
- **File Management**: Users can upload HTML files to the server's designated directory.
- **Logging**: Each server instance maintains a log of interactions for monitoring purposes.
```
## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/unaveragetech/server_head.git
   cd server_head
   ```

2. **Install dependencies**:
   This project requires Flask and Flask-Login. The script will automatically install these packages if they are not present:
   ```bash
   python script.py
   ```

3. **Verify the installation**: 
   Ensure that Flask and Flask-Login are installed correctly by checking the output during the initial run.

## Usage

1. **Run the server manager**:
   ```bash
   python script.py
   ```

2. **Open a web browser** and navigate to:
   ```
   http://localhost:<port>/login
   ```
   Replace `<port>` with the port number assigned to your server instance (e.g., `5001`, `5002`, etc.).

3. **Log in** using one of the following accounts:
   - Admin: `admin` / `admin_password`
   - Superuser: `superuser` / `superuser_password`
   - User: `user` / `user_password`

4. **Manage your server** from the admin panel:
   - Upload files to the server.
   - Check the server status.
   - Restart the server (superuser only).

## Configuration

You can modify user credentials and server settings directly in the script:

- **Users**: Change the `users` dictionary to add or modify user accounts, passwords, roles, and instance names.
- **Secret Key**: Adjust the `secret_key` for session management to enhance security.
- **Port Assignment**: The script assigns unique ports starting from `5001`. Adjust this as needed for your environment.

## User Roles and Permissions

- **User**: 
  - Can upload files to their instance.
  - Can view their own files.
- **Admin**:
  - Can upload files.
  - Can check server status.
  - Cannot restart the server.
- **Superuser**:
  - All admin permissions.
  - Can restart the server.

## File Management

- Users can upload HTML files through the web interface.
- Uploaded files are stored in a designated directory for each server instance (`server_<id>/html_files`).
- Users must have appropriate roles to perform file uploads.

## Logging

- Each server instance maintains a log file named `server_<id>.log`.
- Logs record significant events, including file uploads and server status checks, helping with monitoring and debugging.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments

- Special thanks to the Flask and Flask-Login communities for their documentation and support.
- Inspiration from various open-source projects.

## Contact

For any questions or feedback, feel free to reach out through the [contact form](https://formsubmit.co/el/sumuhu).
```

### Instructions

1. Save the above content into a file named `README.md` in your project root directory.
2. Make sure your GitHub repository is updated with this README.

This version includes your repository link and a contact form for feedback, along with detailed information about the project. Let me know if you need further modifications!
