# Notes application

The NoteKeeper project is a web application designed to help users organize their notes efficiently. 
Users can access the main page where they can view existing notes, add new notes, edit, archive, or 
delete specific notes.

## Access the Project

You can access the Notes app project by this url http://159.223.234.162/.

## Features

- User Authentication: Each user has their own account, ensuring that their notes are private and accessible only to them.
- View Existing Notes: Users can view a list of existing notes on the main page.
- Add New Note: Users can add a new note.
- Edit Note: Users can edit an existing note, updating its text content and category if necessary.
- Archive Note: Users can archive specific notes, which moves them to a separate archived section.
- Delete Note: Users can permanently delete a note if they no longer need it.
- Category Management: Users can categorize their notes by assigning them to specific categories. 
- Sort Notes: Users can sort notes by creation date, total word count, unique word count, or category.


## Technologies Used

The "978.ua" project is developed using the following technologies:

- Django: Python-based web framework for building web applications.
- HTML/CSS/JavaScript/jQuery: For frontend development and user interaction.
- Database: SqLite
## Usage Instructions

Python must be already installed.

1. **Installation:**
    - Clone the repository to your local machine `https://github.com/IlyaGrynyshyn/notes-app`.
    - Create virtual environment `python3 -m venv venv`
    - Install the required dependencies using `pip install -r requirements.txt`.

2. **Running:**
    - Apply migrations `python manage.py migrate`
    - Start the server with `python manage.py runserver`.
    - Access the store via `http://localhost:8000` in your web browser.

3. **Registration/Login:**
    - To access all functionalities of the project, create super user and log in to your account.


## Docker

To run the Notes App project using Docker Compose:
- Start the containers: `docker-compose up --build`
- Access the application at http://localhost:8000

## Test User
   - login: admin
   - password: admin

## Developer Commands

- `python manage.py makemigrations`: Create database migrations.
- `python manage.py migrate`: Apply migrations to the database.
- `python manage.py createsuperuser`: Create a site administrator.

## Running Tests

To run tests for the Notes project use the Django management command: `python manage.py test`
