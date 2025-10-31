# CODERR – Freelancer Platform API

A RESTful backend built with **Django** and **Django REST Framework** for a freelancer marketplace where users can **post offers**, **create orders**, **leave reviews**, and **manage profiles**.

---

## Key Features

* **User Authentication** – Token-based authentication with registration and login
* **Dual Profile Types** – Business users (freelancers) and Customer users (clients)
* **Offers System** – Freelancers create offers with 3 pricing tiers (Basic, Standard, Premium)
* **Orders Management** – Customers can order services with status tracking
* **Reviews & Ratings** – Customers can review business users (1-5 stars)
* **File Upload** – Profile picture support for users
* **Platform Statistics** – Public endpoint for platform metrics
* **API Rate Limiting** – Throttling to prevent abuse
* **Pagination** – Efficient data loading for large datasets

---

## Technical Stack

* **Backend:** Django 5.x + Django REST Framework
* **Database:** SQLite (development) / PostgreSQL (production ready)
* **Authentication:** Token-based (DRF TokenAuthentication)
* **File Storage:** Local media files (configurable for S3)
* **Testing:** Django TestCase with APIClient
* **API Design:** RESTful with modular app structure

---

## Project Structure
```
CODERR/
├── core/                         # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── authentication/               # User registration & login
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   └── models.py
│
├── profiles/                     # User profiles (Business & Customer)
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── models.py
│   └── permissions.py
│
├── offers/                       # Freelancer offers with pricing tiers
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   └── models.py
│
├── orders/                       # Order management & status tracking
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── models.py
│   └── permissions.py
│
├── reviews/                      # User reviews and ratings
│   ├── api/
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests/
│   ├── models.py
│   └── permissions.py
│
├── media/                        # Uploaded files (profile pictures, etc.)
├── env/                          # Virtual environment (ignored in Git)
├── manage.py
├── db.sqlite3
├── requirements.txt
└── README.md
```

---

## Setup Guide

### Prerequisites

* Python 3.11+
* pip
* Git

---

### Installation

**1️⃣ Clone the repository**
```bash
git clone https://github.com/domcamillo/coderr.git
cd coderr-backend
```

**2️⃣ Create and activate a virtual environment**
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

**3️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

**4️⃣ Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5️⃣ Create a superuser (optional)**
```bash
python manage.py createsuperuser
```

**6️⃣ Start the development server**
```bash
python manage.py runserver
```

Your API is now available at:
 **http://127.0.0.1:8000/**

Admin panel:
 **http://127.0.0.1:8000/admin/**

---

## API Overview

### Authentication

| Method | Endpoint              | Description           | Auth Required |
|--------|-----------------------|-----------------------|---------------|
| POST   | `/api/registration/`  | Register new user     | No            |
| POST   | `/api/login/`         | Login and get token   | No            |

### Profiles

| Method | Endpoint                  | Description                | Auth Required |
|--------|---------------------------|----------------------------|---------------|
| GET    | `/api/profile/{id}/`      | Get profile details        | Yes           |
| PATCH  | `/api/profile/{id}/`      | Update profile             | Yes (Owner)   |
| DELETE | `/api/profile/{id}/delete-image/` | Delete profile picture | Yes (Owner) |
| GET    | `/api/profiles/business/` | List all business profiles | No            |
| GET    | `/api/profiles/customer/` | List all customer profiles | No            |

### Offers

| Method | Endpoint          | Description              | Auth Required      |
|--------|-------------------|--------------------------|---------------------|
| GET    | `/api/offers/`    | List all offers          | Yes                 |
| POST   | `/api/offers/`    | Create offer (3 tiers)   | Yes (Business only) |
| GET    | `/api/offers/{id}/` | Get offer details      | Yes                 |
| PATCH  | `/api/offers/{id}/` | Update offer           | Yes (Owner)         |
| DELETE | `/api/offers/{id}/` | Delete offer           | Yes (Owner)         |

### Orders

| Method | Endpoint                  | Description                   | Auth Required       |
|--------|---------------------------|-------------------------------|---------------------|
| GET    | `/api/orders/`            | List user's orders            | Yes                 |
| POST   | `/api/orders/`            | Create order                  | Yes (Customer only) |
| GET    | `/api/orders/{id}/`       | Get order details             | Yes (Owner)         |
| PATCH  | `/api/orders/{id}/`       | Update order status           | Yes (Business only) |
| DELETE | `/api/orders/{id}/`       | Delete order                  | Yes (Admin only)    |
| GET    | `/api/order-count/{user_id}/` | Count active orders       | Yes                 |
| GET    | `/api/completed-order-count/{user_id}/` | Count completed orders | Yes       |

### Reviews

| Method | Endpoint            | Description          | Auth Required        |
|--------|---------------------|----------------------|----------------------|
| GET    | `/api/reviews/`     | List all reviews     | Yes                  |
| POST   | `/api/reviews/`     | Create review        | Yes (Customer only)  |
| PATCH  | `/api/reviews/{id}/`| Update review        | Yes (Owner only)     |
| DELETE | `/api/reviews/{id}/`| Delete review        | Yes (Owner only)     |

**Query Parameters:**
- `?business_user={id}` - Filter reviews by business user
- `?reviewer={id}` - Filter reviews by reviewer
- `?ordering=rating` - Sort by rating
- `?ordering=-updated_at` - Sort by newest first

### Platform Statistics

| Method | Endpoint          | Description               | Auth Required |
|--------|-------------------|---------------------------|---------------|
| GET    | `/api/base-info/` | Platform statistics       | No            |

**Response:**
```json
{
  "review_count": 150,
  "average_rating": 4.6,
  "business_profile_count": 45,
  "offer_count": 200
}
```

---

## Authentication

The API uses **Token Authentication**. After login/registration, include the token in request headers:
```
Authorization: Token your_token_here
```

**Example with curl:**
```bash
curl -H "Authorization: Token abc123..." http://127.0.0.1:8000/api/orders/
```

---


## Key Dependencies

* `Django` - Web framework
* `djangorestframework` - REST API toolkit
* `django-cors-headers` - CORS handling
* `django-filter` - Query filtering

See `requirements.txt` for complete list.

---

## Business Logic

### User Types

* **Business Users** - Freelancers who create offers and receive orders
* **Customer Users** - Clients who browse offers and place orders

### Offer Structure

Each offer has **3 pricing tiers**:
- **Basic** - Entry-level service
- **Standard** - Mid-tier with more features
- **Premium** - Full-featured service

### Order Workflow

1. Customer selects an offer detail (Basic/Standard/Premium)
2. Order is created with `in_progress` status
3. Business user works and updates status
4. Possible statuses: `in_progress`, `delivered`, `completed`, `cancelled`

### Review System

* Only customers can leave reviews
* Only business users can be reviewed
* One review per customer-business pair (unique constraint)
* Rating: 1-5 stars

---

## Configuration

### Media Files
```python
# settings.py
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

### Pagination
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### Throttling
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'login': '5/minute'
    }
}
```

---

## Frontend Integration

This backend is designed to work with a **vanilla JavaScript** frontend.

**CORS is configured** to allow frontend requests during development.

---

## Development Notes

* Use `.env` file for sensitive settings (not included in Git)
* SQLite for development, PostgreSQL recommended for production
* All models use `created_at` and `updated_at` timestamps
* File uploads stored in `/media/uploads/`
* Admin interface available at `/admin/`

---

## License

MIT License © 2025 Dominic Mörth

---

## Author

**Dominic Mörth**

* GitHub: [@DomCamillo](https://github.com/domcamillo)
* Email: dominic@moerth.ch

---

## Acknowledgments

* Django & Django REST Framework documentation
* Developer Akademie for project guidance

---

**Built with ❤️ using Django REST Framework**