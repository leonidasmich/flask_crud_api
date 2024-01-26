### API DOCS

# Running the Flask Application
- Install Required Python Packages:
`pip install -r requirements.txt`
- Configure Database
- Run Flask app:
`python app.py`

# Running the Flask Application using Docker for Production using gunicorn
- Set `app.run(debug=False)`
- Run `docker build -t app .`
- Run `docker run -p 8000:8000 app`

# Base URL
The base URL for the API is 'http://localhost:5000/'

# Authentication
All API requests require the use of an authentication token. Include this token in the request header. Example:
` Authorization: AUTH_TOKEN `

## Endpoints
# Get All Users
- URL: `/users`
- Method: `GET`
- Auth Required: Yes
- Description: Retrieves a list of all users.
- Response Example:
```json
[
    {"id": 1, "name": "John", "email": "john@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
] 
```

# Get User by ID
- URL: `/users/<id>`
- Method: `GET`
- Auth Required: Yes
- Description: Retrieves a specific user by their ID.
- URL Parameters: `id=[integer]`
- Response Example:
```json
    {"id": 1, "name": "John", "email": "john@example.com"}
```

# Add a New User
- URL: `/users`
- Method: `POST`
- Auth Required: Yes
- Description: Adds a new user to the database.
- Data Contrains:
```json
{
    "name": "[alphanumeric string]",
    "email": "[valid email address]"
}
```
- Response Example:
```json
    {"message": "User added", "user": {"id": 3, "name": "Alice", "email": "alice@example.com"}}
```

# Update a User
- URL: `/users/<id>`
- Method: `PUT`
- Auth Required: Yes
- Description: Updates the details of an existing user.
- URL Parameters: `id=[integer]`
- Data Constrains:
```json
{
    "name": "[alphanumeric string]",
    "email": "[valid email address]"
}
```
- Response Example:
```json
    {"message": "User updated"}
```

# Delete a User
- URL: `/users/<id>`
- Method: `DELETE`
- Auth Required: Yes
- Description: Deletes a user form the database.
- URL Parameters: `id=[integer]`
- Response Example:
```json
    {"message": "User Deleted"}
```

## Error Handling
The API uses conventional HTTP response codes to indicate success or failure of an API request. In general:
- Codes in the `2xx` range indicate success.
- Codes in the `4xx` range indicate an error due to the informations provided.
- Codes in the `5xx` range indicate an error with our server.

# Notes
- Ensure the MySQL database is running and is accessible for the API to function correctly.
- Replace the base URL, port and authorization token as necessary according to your deployment configuration.


