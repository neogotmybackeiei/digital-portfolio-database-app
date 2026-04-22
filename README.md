# Portfolio (Django + PostgreSQL)

A CRUD app to catalog portfolio works (with multiple file uploads per work)
and present them as a public showcase, timeline, and filterable archive.

## Features
- Add / edit / delete works with title, description, keywords, **work date**,
  category (dropdown), external link, and **multiple file uploads** per entry
  (PDF / PNG / JPG / JPEG, max 10MB each).
- **Showcase** page grouped by category with **top 3 pinned** featured works.
- **Filter** page: keyword search, category, date range, file type.
- **Timeline** view of all work, newest → oldest.
- White + mint green theme, Inter + Fraunces fonts.

## Setup (VS Code, macOS / Linux / Windows)

1. Open the folder in VS Code, then in the integrated terminal:

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set your Postgres connection URL:

   ```
   DATABASE_URL=postgres://user:password@localhost:5432/portfolio
   SECRET_KEY=any-long-random-string
   DEBUG=True
   ```

3. Create the database tables (this is the step that fixes
   `relation "works_work" does not exist`):

   ```bash
   python manage.py makemigrations works
   python manage.py migrate
   ```

4. (Optional) create an admin user for `/admin/`:

   ```bash
   python manage.py createsuperuser
   ```

5. Seed the category dropdown with some defaults:

   ```bash
   python manage.py seed_categories
   ```

6. Run the server:

   ```bash
   python manage.py runserver
   ```

   Open http://127.0.0.1:8000/

## URLs
- `/` → public showcase (grouped by category, pinned top 3 at top)
- `/timeline/` → chronological timeline
- `/filter/` → filterable archive
- `/works/` → manage entries (list)
- `/works/add/` → new entry
- `/admin/` → Django admin
