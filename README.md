

#  Ferrum Logistica

**Ferrum Logistica** is a web application for managing maritime shipping logistics. It is built with Django and provides features for users to create shipping contracts, manage ports and ships, assign contracts, generate shipping routes, and visualize financial and operational statistics.

---

##  Features

###  User Functionality
- User registration and login
- Creating shipping contracts
- Specifying cargo type, quantity, and temperature requirements
- Selecting departure and destination ports
- Making contract payments
- Viewing order history and payment status

###  Admin Functionality
- Full control panel for managing:
  - Ports (Create, Edit, Delete)
  - Ships (Create, Edit, Delete, Repair)
  - Assignments of contracts to ships
  - Route generation between ports
- Marking routes as completed
- Calculating and registering crew payments
- Data-driven charts and statistics

---

## Visualizations

Integrated with **Plotly**, the app displays:
- Cargo distribution by type (pie chart)
- Monthly statistics for:
  - Payments
  - Ship repairs
  - Crew payments

---

##  Key Pages

| Route                 | Description                         |
|----------------------|-------------------------------------|
| `/`                  | Home page with company info         |
| `/register`          | User registration                   |
| `/login`             | Login page                          |
| `/area`              | User dashboard for orders & payments|
| `/contact`           | Overview of paid contracts          |
| `/statistics`        | Interactive statistics and graphs   |
| `/admin_panel`       | Admin control panel                 |
| `/port`              | Port management                     |
| `/ship`              | Ship management and repairs         |
| `/route_ships_page`  | Route visualization and control     |

---

##  Technologies Used

- **Backend**: Django 2.1+
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Charts**: Plotly (Python)
- **Database**: PostgreSQL
- **User Auth**: Custom Django User Model
- **Geolocation**: geopy for distance calculations

---

##  Getting Started

### Requirements
- Python 3.6+
- PostgreSQL
- Virtualenv (optional but recommended)

### Installation

```bash
git clone https://github.com/your-username/ferrum-logistica.git
cd ferrum-logistica
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Setup Database

Make sure PostgreSQL is running and update `settings.py` with your DB credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

---

##  Testing

Unit tests can be run using:

```bash
python manage.py test
```

