# Impactree_API

## Overview

Impactree_API is a Django RESTful API using the Django Rest Framework. It serves as the back-end of the Impactree full-stack web application for tracking philanthropic donations and their impact. The system allows users to manage their donations, view various charities, and track their progress through a tree-based milestone system.

## Technology Used

- Python
- Django
- Django Rest Framework
- SQLite

## Learning Objectives

- Implement a RESTful API using Django and Django Rest Framework
- Design and implement a database schema for tracking donations and user progress
- Test-Driven Development through automated integration tests
- Integrate user authentication and authorization
- Apply best practices for data modeling and API design

## Project Goals

1. Implement user authentication using Django's token-based authentication system
2. Allow customers to delete their own data while preventing access to others' data
3. Enable customers to edit their own data while restricting access to others' information
4. Utilize Django as the major framework for the project
5. Create a scalable and maintainable API structure
6. Implement proper data validation and error handling

## Installation Instructions

1. Clone the repository:
    ```sh
   git clone <repository-url>
   cd <project-directory>

2. Create a virtual environment:
    ```sh
    pipenv shell

3. Install the required packages:
    ```sh
   pipenv install

4. Set up & seed the database:
    ```sh
   rm db.sqlite3
    rm -rf ./impactreeapi/migrations
    python3 manage.py migrate
    python3 manage.py makemigrations impactreeapi
    python3 manage.py migrate impactreeapi
    python3 manage.py loaddata users
    python3 manage.py loaddata tokens

6. Run the development server:
    ```sh
   python manage.py runserver

7. Access the API at `http://localhost:8000`

## API Endpoints

(Return & List API endpoints here)

## Data Models

The project includes the following main models:

- User (Django's built-in user model)
- Profile (extends User with additional fields)
- CharityCategory
- Charity
- Donation
- TreeMilestone
- UserTreeProgress

For a detailed view of the data structure, please refer to the ERD (Entity-Relationship Diagram) in the project documentation.

## Testing

To run the test suite:

```sh
python manage.py test tests -v 1