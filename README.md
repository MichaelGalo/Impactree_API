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
- Implement proper data validation and error handling

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
    python3 manage.py migrate
    python3 manage.py makemigrations impactreeapi
    python3 manage.py migrate impactreeapi
    python3 manage.py loaddata users
    python3 manage.py loaddata tokens
    python3 manage.py loaddata milestones
    python3 manage.py loaddata impactplans
    python3 manage.py loaddata charitycategories
    python3 manage.py loaddata charities
    python3 manage.py loaddata impactplan_charities

6. Run the development server:
    ```sh
   python manage.py runserver

7. Access the API at `http://localhost:8000`

## API Endpoints (MVP)
- register
- login
- users
- milestones
- charitycategories
- charities
- impactplans

## Data Models

The project includes the following main models:

- User (Django's built-in user model)
- Tokens (Django's built-in tokens)
- ImpactPlan
- CharityCategory
- Charity
- ImpactPlanCharity (many-to-many join table)
- Milestone

For a detailed view of the data structure, please refer to the ERD (Entity-Relationship Diagram) in the project documentation.

## Testing

To run the test suite:

```sh
python manage.py test tests -v 1