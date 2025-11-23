# Deployment Guide

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize database:
   ```bash
   python seed_data.py
   ```

3. Run the development server:
   ```bash
   python app.py
   ```

4. Access at `http://localhost:5000`

## Production Deployment Options

### Option 1: PythonAnywhere (Recommended for Students)

1. Create a free account at [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your files via the Files tab
3. Create a new web app with Flask framework
4. Configure WSGI file to point to your app.py
5. Install dependencies via Bash console:
   ```bash
   pip install --user -r requirements.txt
   ```
6. Initialize database:
   ```bash
   python seed_data.py
   ```
7. Reload the web app

### Option 2: Heroku

1. Create a `Procfile`:
   ```
   web: python app.py
   ```

2. Add to requirements.txt:
   ```
   gunicorn==21.2.0
   ```

3. Update app.py to use PORT environment variable:
   ```python
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

4. Deploy:
   ```bash
   heroku create
   git push heroku master
   ```

### Option 3: Render

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Add environment variables if needed
6. Deploy

## Database Considerations

For production, consider migrating from SQLite to:
- PostgreSQL (for Heroku/Render)
- MySQL (for PythonAnywhere)

Update the database connection string in app.py accordingly.

## Security Notes

- Change all default passwords
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement proper authentication (JWT tokens)
- Add input validation and sanitization
