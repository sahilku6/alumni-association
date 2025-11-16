# Detailed Installation Guide

## System Requirements
- Python 3.8+
- pip
- Git
- 500MB free disk space

## Windows Installation

### Step 1: Install Python
- Download from python.org
- Check "Add Python to PATH"
- Verify: `python --version`

### Step 2: Clone Repository
```bash
git clone https://github.com/yourusername/alumni-association.git
cd alumni-association
```

### Step 3: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Admin User
```bash
python manage.py createsuperuser
```

### Step 7: Run Server
```bash
python manage.py runserver
```

## macOS Installation

### Step 1: Install Python
```bash
brew install python3
```

### Step 2: Clone Repository
```bash
git clone https://github.com/yourusername/alumni-association.git
cd alumni-association
```

### Step 3: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5-7: Same as Windows (Steps 5-7)

## Linux Installation

### Step 1: Install Python & Dependencies
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
```

### Step 2-7: Same as macOS (Steps 2-7)

## Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Register**: http://127.0.0.1:8000/register/
