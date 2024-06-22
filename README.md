- set up database
  > create mysql database 'rental_app'
  > import rental.sql
  
- create virtual environment
  > python -m venv ven
  
  > ven\Scripts\activate

- Install library
  > pip install -r requirements.txt

- run app
  > uvicorn app.main:app  --reload
