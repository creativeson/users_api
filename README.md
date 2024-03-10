1. Create User
Endpoint: POST /users
Description: Create a new user.
Request Body:
- name (str): Name of the user.
- email (str): Email of the user.
- password (str): Password of the user.
Response:
- message (str): Confirmation message.
Status Codes:
- 201: User created successfully.
- 400: Email already registered.
2. Get User
Endpoint: GET /users/{user_id}
Description: Retrieve user information by user ID.
Path Parameters:
- user_id (int): ID of the user to retrieve.
Response:
- User information (JSON).
Status Codes:
- 200: User found and returned.
- 404: User not found.
3. Update User
Endpoint: PUT /users/{user_id}
Description: Update user information.
Path Parameters:
- user_id (int): ID of the user to update.
Request Body:
- name (str): New name of the user.
- email (str): New email of the user.
- password (str): New password of the user.
Response:
- message (str): Confirmation message.
Status Codes:
- 200: User updated successfully.
4. Delete User
Endpoint: DELETE /users/{user_id}
Description: Delete a user by user ID.
Path Parameters:
- user_id (int): ID of the user to delete.
Response:
message (str): Confirmation message.
Status Codes:
- 200: User deleted successfully.
5. User Login
Endpoint: POST /login
Description: Authenticate user and generate JWT token.
Request Body:
- email (str): Email of the user.
- password (str): Password of the user.
Response:
token (str): JWT token.
Status Codes:
- 200: Login successful.
- 401: Invalid email or password.
6. Retrieve Current User
Endpoint: GET /member
Description: Retrieve information of the currently authenticated user.
Authorization: Bearer Token.
Response:
User information (JSON).
Status Codes:
- 200: User found and returned.
- 401: Unauthorized (Missing or invalid token).
- 404: User not found.





