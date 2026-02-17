# Odoo 19 Setup & Employees CRUD via Python JSON-RPC

This guide shows how to **install Odoo 19 Community Edition on Ubuntu 24.04 LTS** and interact with it programmatically using **Python and JSON-RPC**.  
It includes a sample Python project to manage **Employee (`hr.employee`) records** (Create, Read, Update, Delete, List) directly via the Odoo API.

> Recommended system: **4 GB RAM minimum (6 GB+ recommended), 2+ CPUs, SSD storage**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Odoo 19 Installation](#odoo-19-installation)
3. [Employees CRUD Python Project](#employees-crud-python-project)
4. [Installation & Setup](#installation--setup)
5. [How to Run](#how-to-run)
6. [Project Structure](#project-structure)
7. [Notes](#notes)
8. [Troubleshooting](#troubleshooting)
9. [Conclusion](#conclusion)

---

## Prerequisites

Before installing Odoo 19:

- Ubuntu 24.04 (64-bit) with **sudo / root** access
- Minimum **4 GB RAM** (6 GB+ recommended)
- At least **20 GB free disk space**
- Internet access
- Python 3.10+ (tested with 3.11)

---

## Odoo 19 Installation

### Step 1 — Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2 — Create Odoo System User

```bash
sudo adduser --system --home=/opt/odoo19 --group odoo19
```

### Step 3 — Install PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib -y
sudo su - postgres -c "createuser --createdb odoo19"
```

> Creates a PostgreSQL user `odoo19` with permissions to create databases.

### Step 4 — Install Dependencies

```bash
sudo apt install git python3 python3-pip python3-venv build-essential \
wget python3-dev libxslt-dev libzip-dev libldap2-dev libsasl2-dev \
libjpeg-dev libpq-dev libxml2-dev libssl-dev libffi-dev -y
```

### Step 5 (Optional) — Install wkhtmltopdf

Needed for PDF reports:

```bash
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.jammy_amd64.deb
sudo apt install ./wkhtmltox_0.12.6-1.jammy_amd64.deb -y
```

> Using the patched build ensures proper headers/footers in PDF reports.

### Step 6 — Download Odoo Source

```bash
sudo su - odoo19
git clone https://github.com/odoo/odoo --depth 1 --branch 19.0 /opt/odoo19/odoo
exit
```

### Step 7 — Python Virtual Environment

```bash
sudo su - odoo19
cd /opt/odoo19
python3 -m venv odoo-venv
source odoo-venv/bin/activate
pip install wheel
pip install -r odoo/requirements.txt
deactivate
exit
```

### Step 8 — Create Odoo Configuration

`/etc/odoo19.conf`:

```ini
[options]
admin_passwd = YOUR_STRONG_ADMIN_PASSWORD
db_host = False
db_port = False
db_user = odoo19
db_password = False
addons_path = /opt/odoo19/odoo/addons
logfile = /var/log/odoo19.log
xmlrpc_port = 8069
```

Set permissions:

```bash
sudo chown odoo19: /etc/odoo19.conf
sudo chmod 640 /etc/odoo19.conf
sudo touch /var/log/odoo19.log
sudo chown odoo19: /var/log/odoo19.log
```

### Step 9 — Systemd Service

create `/etc/systemd/system/odoo19.service`:

```ini
[Unit]
Description=Odoo 19
Requires=postgresql.service
After=network.target postgresql.service

[Service]
Type=simple
SyslogIdentifier=odoo19
PermissionsStartOnly=true
User=odoo19
Group=odoo19
ExecStart=/opt/odoo19/odoo-venv/bin/python3 /opt/odoo19/odoo/odoo-bin -c /etc/odoo19.conf
StandardOutput=journal+console

[Install]
WantedBy=multi-user.target
```

Enable and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now odoo19
sudo systemctl start --now odoo19
sudo systemctl status odoo19
```

Verify installation:

```bash
sudo ss -lntp | grep 8069
```

Expected output:

```bash
LISTEN 0.0.0.0:8069
```

### Step 10 — Access Odoo

Open a browser:

```
http://localhost:8069
```

---

## Employees CRUD Python Project

A **Python project** demonstrating CRUD operations on **Odoo Employees (`hr.employee`)** using **JSON-RPC**.  

Features:

- **Create** a new employee
- **Read** an employee by ID
- **Update** employee info
- **Delete** an employee
- **List** employees (name & job_title)

---

## Installation & Setup

1. Clone the repository:

```bash
git clone [<REPOSITORY_URL>](https://github.com/MohamedTestouri/odoo19_setup_and_employees_crud_via_python_json-rpc.git)
cd odoo_poc
```

2. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure `config.py`:

```python
ODOO_URL = "http://localhost:8069/jsonrpc"  # or your server IP/domain
DB_NAME = "your_odoo_db"
USERNAME = "admin"
PASSWORD = "admin"
```

---

## How to Run

```bash
python main.py
```

Expected output:

```bash
Created: 36
Read: [{'id': 36, 'name': 'John Doe', 'job_title': 'Software Engineer'}]
Updated
All employees: [ ... , {'id': 36, 'name': 'John Doe', 'job_title': 'Senior Software Engineer'}]
Deleted
```

---

## Project Structure

```
odoo_poc/
│
├── config.py             # Odoo connection settings
├── rpc_client.py         # JSON-RPC client
├── employee_service.py   # Employee CRUD service
├── main.py               # Demo script showing CRUD operations
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Notes

- Uses **JSON-RPC** instead of XML-RPC for communication.
- Requires **`hr` module (Employees)** installed in Odoo.
- No GUI or database migration needed — works directly via API.

---

## Troubleshooting

- **Connection error** → Check Odoo URL, DB name, and credentials.
- **Missing `hr.employee` field** → Ensure **Employees module** is installed.
- **Permission errors** → Run commands with `sudo` where required.

---

## Conclusion

- This guide demonstrates **Odoo 19 installation** on Ubuntu 24.04 and **programmatic interaction** via Python JSON-RPC.
- Employees CRUD project allows you to **manage employee records** without using Odoo UI.
- Provides a foundation for **automation, integrations, or custom module development**.
- Easily extendable to other Odoo models or business workflows.

