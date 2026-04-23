# Portfolio (Django + PostgreSQL)

A CRUD app to catalog portfolio works (with multiple file uploads per work)
and present them as a public showcase, timeline, and filterable archive.

## Reflection

I wanted to build an app where you can upload all of your digital works, including academic writing and photography, to one place so that you can build a comprehensive portfolio of academic and nonacademic work. You can add an entry and fill out fields like description, category of work, and keywords. Then you upload one or more media files that are supported (pdf, jpeg, png) and add the entry to the database. You are able to view all entries, update or delete an entry. There is also a showcase page where you can see all the works grouped by category. 

At the top there is a “Featured” section where you can pin your top three works across all entries. There is also a page called “Timeline” that gives a comprehensive timeline of all the work entered with the date it was completed, title, part of the description and a thumbnail of the media file. Another page is the “Filtered” page where you can search for specific works based on keywords, the title, description, by category, by date, and by file type. 

Everything I asked Lovable for in my planning phase worked. It was kind of confusing to initialize and prep the environment in the VS Code terminal but it created a good layout with the color scheme I wanted. It completed all of the functions I wanted. Granted, I had to do it all over again because I did not plan it out enough the first time. That is one thing I would do differently is have a more concrete plan of what I want before I ask a LLM to create the Django code. I was having issues with the Postgres database where when I launched the second version it was having trouble creating the tables because it already existed for the first attempt. 

Another thing I would do differently if I had more time is add more design and personality to the app. The final version has the color scheme I want and I like the ombre effect in the “Featured” section box but it is a little too simple for me if I wanted to actually use this regularly. I would like to have a personalized logo for the “Portfolio” title in the top left corner like many companies do with their own websites. Also maybe add some more texture or color into the background or buttons.


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
