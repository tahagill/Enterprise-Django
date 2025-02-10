\# Enterprise

Enterprise is a full-stack web application built using Django, with PostgreSQL as the database. It integrates both backend and frontend functionalities, offering a scalable and efficient web development architecture.

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** 
- **Database:** PostgreSQL
- **Authentication:** (using Oauth2 and JWT)

## 📦 Features

- Full-stack Django web application
- Scalable backend with PostgreSQL database integration
- User authentication (using Oauth2 and JWT)
- Static and media file handling
- Customizable settings for different environments

## 🚀 Setup & Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/tahagill/Enterprise-Django.git
    cd Enterprise-Django
    ```

2. **Create a virtual environment & activate it:**

    ```bash
    python -m venv env
    # On Windows:
    env\Scripts\activate
    # On macOS/Linux:
    source env/bin/activate
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the PostgreSQL database:**

    - Update your database settings in `settings.py` (configure your PostgreSQL database credentials).
    - Run the migrations to create the necessary tables:

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the app in your browser:**

    Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the app.

    Access the admin panel at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) using the superuser credentials.
