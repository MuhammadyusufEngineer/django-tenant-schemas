# Mini Multitenant Django App

A simple multitenant Django app demonsrating tenant specifig configuration retrieveal via file-based JSON configs,
with feature toggling API endpoints

## Tech stack

- Python 3.x
- Django 3.2.17
- django-tenant-schemas 1.12.0
- Django REST Framework 3.12.4

# Project structure

```bash
myproject/
├── configs/
│ ├── tenant_a_config.json
│ └── tenant_b_config.json
├── myproject/
├── tenants/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── serializers.py
│ └── tests.py
├── manage.py
├── requirements.txt
└── README.md
```

# 🚀 Setup & Run Instructions

1️⃣ **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate
```

# 2️⃣ Install dependencies

pip install -r requirements.txt

# 3️⃣ Run migrations

python manage.py migrate

# 4️⃣ Create config files

Inside configs/:

tenant_a_config.json
tenant_b_config.json

Example:

{
"tenant_id": "a",
"enable_custom_page": true,
"page_title": "Welcome Tenant A"
}

# 5️⃣Run the development server:

python manage.py runserver

| Method | Endpoint                        | Description                                                 |
| :----- | :------------------------------ | :---------------------------------------------------------- |
| GET    | `/api/tenants/<id>/`            | Get tenant details                                          |
| GET    | `/api/config/<tenant_id>/`      | Fetch tenant’s config JSON                                  |
| GET    | `/api/config/<tenant_id>/page/` | Show page title if `enable_custom_page` is `true`, else 403 |

# 🧪 Running Tests

```bash
python manage.py test
```

# 📌 Notes

- Config files are loaded from /configs/.
- Tenant A cannot access Tenant B’s config (file-based isolation).
- Returns appropriate 404 and 403 errors for missing configs or disabled pages.
