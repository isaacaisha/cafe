# ☕ Café Explorer

A **Flask**-powered web app for discovering, adding, and managing cafés around you. Features user registration, role-based admin controls, search functionality, and rich data management with Flask extensions and a sleek Bootstrap UI.

![Platform Demo](static/assets/images/cafe.webp)

---

## 🌟 Core Features

* 🔍 Search cafés by location
* 🎲 Random café picker
* ➕ Add, update, and delete café entries (admin-only)
* 👤 User authentication & registration
* 🔐 Admin vs. user role management
* 📊 Café details: name, location, seating, amenities, pricing
* ☑️ WTForms for secure, validated forms
* 🗓️ Date display with UTC time awareness

---

## 🛠 Technology Stack

| Component               | Purpose                            |
| ----------------------- | ---------------------------------- |
| Flask                   | Web framework                      |
| Flask-SQLAlchemy        | ORM for database interactions      |
| Flask-Migrate           | Database migrations                |
| Flask-Login             | Session & user auth                |
| Flask-WTF & CSRFProtect | Form handling & security           |
| Flask-Bootstrap         | Responsive UI styling              |
| Werkzeug.security       | Password hashing                   |
| SQLite (default)        | Development database               |
| PostgreSQL / Redis      | (Optional production alternatives) |
| Gunicorn                | WSGI server for deployment         |
| Alembic                 | Schema migrations                  |

---

## 📂 Project Structure

```plaintext
📦 cafe-explorer/
├── app.py                  # Main application entry
├── forms.py                # WTForms definitions
├── models.py (in-app)      # SQLAlchemy models
├── templates/              # Jinja2 templates
│   ├── index.html
│   ├── cafe_detail.html
│   └── ...
├── static/                 # Static assets (CSS/JS/Images)
├── migrations/             # Flask-Migrate files
├── requirements.txt        # Python dependencies
└── README.md               # This documentation
```

---

## ⚙️ Installation & Setup

1. **Clone repo**

   ```bash
   ```

git clone [https://github.com/isaacaisha/cafe-explorer.git](https://github.com/isaacaisha/cafe-explorer.git)
cd cafe-explorer

````
2. **Create & activate venv**
   ```bash
python3 -m venv venv
source venv/bin/activate
````

3. **Install dependencies**

   ```bash
   ```

pip install -r requirements.txt

````
4. **Configure environment**
   ```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:pass@host/dbname"  # optional
````

5. **Initialize database**

   ```bash
   ```

flask db init
flask db migrate
flask db upgrade

````
6. **Run the server**
   ```bash
flask run
````

---

## 🔑 Admin Operations

* **Add café**: `POST /add` (admin only)
* **Update price**: `PATCH /update-price/<id>`
* **Delete café**: `POST /delete-cafe`
* **Delete user**: `POST /delete-user`

> Use the secret admin code `siisi321` on login to elevate your role.

---

## 📦 Dependencies

```text
aio-timeout==5.0.1
alembic==1.11.1
blinker==1.6.2
click==8.1.3
dnspython==2.7.0
dominate==2.8.0
email_validator==2.2.0
Flask==2.3.2
Flask-Bootstrap==3.3.7.1
Flask-Login==0.6.2
Flask-Migrate==4.0.4
Flask-SQLAlchemy==3.0.3
Flask-WTF==1.1.1
greenlet==2.0.2
gunicorn==21.2.0
idna==3.10
itsdangerous==2.1.2
Jinja2==3.1.2
Mako==1.2.4
MarkupSafe==2.1.2
packaging==23.1
psycopg2==2.9.6
redis==4.6.0
SQLAlchemy==1.4.18
Werkzeug==2.3.4
WTForms==3.0.1
```

---

## 🤝 Contributing

Contributions welcome! Please fork and submit pull requests. For major changes, open an issue first.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Isaac Aïsha** — [@isaacaisha](https://github.com/isaacaisha)

Enjoy exploring cafés! ☕🎉
