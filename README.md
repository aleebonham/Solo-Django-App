# Solo-Django-App Alee Bonham
Project for assessment 3 programming exercise - Enterprise Software

Online Bookstore Application with book data coming from an Open Date Source.
Allows for book browsing, adding to cart, checkout function, user authentication, profile creation, and an admin dashboard.

Deployment
Cloud Deployment URL: https://aleebonham.pythonanywhere.com
Github Repository: https://github.com/aleebonham/Solo-Django-App.git

This application is deployed on PythonAnywhere
-Django 3.2.18 with Python 3.10
-Manual configuration with a virtual environment

Features
Browse and search books by title, author, or genre.
Add books to cart and checkout.
User registration, login, and admin dashboard.
Admin dashboard with sales chart using Chart.js 2.9.4.
Dataset of 5,000 book records from Open Library.

Installation:

git clone https://github.com/aleebonham/Solo-Django-App.git, cd Solo-Django-App, python3 -m venv venv, source venv/bin/activate, pip install -r
requirements.txt, python manage.py migrate, python manage.py createsuperuser, python manage.py load_data, python manage.py runserver
0.0.0.0:8000

User:
Users must register and log in to place orders.
They can:
View book catalog, Add/remove books from cart, Place orders
Admins can:
View stats and users, Add/edit/delete books, Export data
Tested for form validation, user roles, and ordering logic.

Development:
Implemented login, registration (UserCreationForm), and user
view protection
Created book browsing, detail views, cart management, and
order placement.
Developed a superuser-only admin dashboard with book, user, and order information.
Designed and linked models: Book, Customer, User, and Order
Secured all views using @login_required and restricted admin tools to superusers

superuser/admin profile info:
Username: admin
Email: admin@example.com
PPassword: bookshop123
