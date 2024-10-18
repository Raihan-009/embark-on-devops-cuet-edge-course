# Flask and systemd Lab Guide

## Introduction
This lab guide walks you through the process of creating a simple Flask web application and deploying it as a systemd service. This setup is commonly used in production environments to ensure your web application starts automatically on system boot and can be easily managed using systemd commands.

## Objectives
By the end of this lab, you will:
1. Create a basic Flask web application
2. Set up a Python virtual environment
3. Use Gunicorn as a WSGI HTTP server
4. Create and configure a systemd service file
5. Deploy and manage your Flask app using systemd

## Expected Outcomes
After completing this lab, you will have:
- A running Flask web application
- A systemd service that manages your application
- The ability to start, stop, and restart your application using systemd commands
- A basic understanding of how to deploy Python web applications in a production-like environment

## Lab Steps

### 1. Set up the environment
```bash
sudo apt update
sudo apt install python3-pip python3-venv
mkdir flask_app
cd flask_app
python3 -m venv venv
source venv/bin/activate
pip install Flask
```

### 2. Create the Flask app
Create a file named `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
```

### 3. Test the app
```bash
python app.py
```
Access http://localhost:5000 in your browser.

### 4. Create a WSGI entry point
Create a file named `wsgi.py`:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

### 5. Install and configure Gunicorn
```bash
pip install gunicorn
```

### 6. Create a systemd service file
Create `/etc/systemd/system/flask_app.service`:

```ini
[Unit]
Description=Gunicorn instance to serve flask app
After=network.target

[Service]
User=<your_username>
Group=<your_group>
WorkingDirectory=/path/to/flask_app
Environment="PATH=/path/to/flask_app/venv/bin"
ExecStart=/path/to/flask_app/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app

[Install]
WantedBy=multi-user.target
```

To fill in the correct values:

- `<your_username>`: Run `whoami` in terminal
- `<your_group>`: Run `groups` and use the first group listed
- `/path/to/flask_app`: Run `pwd` in your flask_app directory
- `/path/to/flask_app/venv/bin`: Run `echo $VIRTUAL_ENV/bin` when your virtual environment is activated

### 7. Start and enable the service
```bash
sudo systemctl start flask_app
sudo systemctl enable flask_app
```

### 8. Check the service status
```bash
sudo systemctl status flask_app
```

### 9. Accessing the app
You can access your app at `http://<your_server_ip>:5000`

Note: Make sure your firewall allows traffic on port 5000 if accessing from another machine.

## Managing the Service

To restart the service:
```bash
sudo systemctl restart flask_app
```

To stop the service:
```bash
sudo systemctl stop flask_app
```

To start the service:
```bash
sudo systemctl start flask_app
```

If you make changes to the service file, reload the daemon:
```bash
sudo systemctl daemon-reload
```

## Conclusion
You have now successfully set up a Flask application as a systemd service. This setup allows for easy management of your application and ensures it starts automatically with your system.