# project_setup.py
import os
import shutil

def create_project_structure():
    directories = [
        'app',
        'app/static/css',
        'app/static/js',
        'app/templates',
        'app/models',
        'app/controllers',
        'app/utils',
        'tests',
        'config'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def move_files():
    # Move main application files
    file_moves = {
        'main.py': 'app/app.py',
        'database_manager.py': 'app/models/database_manager.py',
        'index.html': 'app/templates/index.html',
        'setup_db.py': 'app/utils/setup_db.py'
    }
    
    for src, dst in file_moves.items():
        if os.path.exists(src):
            shutil.move(src, dst)

def create_config_file():
    config_content = """
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///phones.db'
    """
    
    with open('config/config.py', 'w') as f:
        f.write(config_content)

def create_init_files():
    init_locations = [
        'app',
        'app/models',
        'app/controllers',
        'app/utils',
        'tests'
    ]
    
    for location in init_locations:
        with open(f'{location}/__init__.py', 'w') as f:
            pass

def main():
    create_project_structure()
    move_files()
    create_config_file()
    create_init_files()
    print("Project structure created successfully!")

if __name__ == "__main__":
    main()