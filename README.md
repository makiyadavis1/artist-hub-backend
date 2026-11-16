# ArtistHub

ArtistHub is a Flask backend application that helps independent music artists organize their promotional tasks.

## Project Overview

ArtistHub is designed to help independent artists manage their music careers in one place. Artists will be able to create, view, update, complete, and delete promotional tasks.

## Planned Features

- Create and manage promotional tasks.
- Track music marketing activities.
- Organize music release promotion.
- Secure artist accounts and private task data.

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite (development database)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/makiyadavis1/artist-hub-backend.git
   cd artist-hub-backend
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up your environment variables (see below).

6. Run the application:

   ```bash
   python run.py
   ```

## Environment Variables

Create a `.env` file by copying `.env.example`:

```bash
cp .env.example .env
```

Update the values in `.env`:

- `DATABASE_URL`: Specifies which database the application connects to. Development currently uses SQLite.
- `JWT_SECRET_KEY`: A private secret key used to secure authentication tokens.

**Important:** Never upload your `.env` file or share your secret key publicly.

## Database Migrations

ArtistHub uses Flask-Migrate to manage database changes.

Once database models have been created, use these commands:

1. Initialize migrations (first time only):

   ```bash
   flask --app run.py db init
   ```

2. Generate a migration after making model changes:

   ```bash
   flask --app run.py db migrate -m "Describe your changes"
   ```

3. Apply migrations to the database:

   ```bash
   flask --app run.py db upgrade
   ```

The migration initialization command only needs to be run once per project. Future database changes generally require the migrate and upgrade commands.