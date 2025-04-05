
# Formlyze Backend

Formlyze Backend is the server-side API that powers the Formlyze platform. It handles form management, user authentication, submissions, and data processing. This backend is built with Django and exposes RESTful APIs to interact with the frontend.






# Installation

#### Clone the repository:

```bash
https://github.com/shakilethicalden/Formlyze.git

```
#### Navigate into the project directory:

```bash
cd formlyze

```
#### Set up a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

```

#### Install project dependencies:

```bash
pip install -r requirements.txt

```

#### Apply database migrations:

```bash
py manage.py makemigrations
py manage.py migrate
```

#### Create a superuser (optional but recommended for admin access):

```bash
py manage.py createsuperuser

```

#### Run the development server:

```bash
py manage.py runserver

```
# Api documentation
## Authentication Endpoints

## User Registration

#### Endpoints
```http
POST /api/users/register/
```

#### Description: 
Register a new user in the system.

#### Request Body:
```bash
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123",
  "healthCareName": "Test Clinic",
  "address": "123 Street, City",
  "phone": "1234567890"
}

````

#### Response(Success (201)):
```bash

{
  "success": true,
  "message": "User registered successfully"
}

````
#### Response(Error (400)):
```bash

{
  "error": "Validation failed"
}

````




## User Login

#### Endpoints
```http
POST /api/users/login/
```

#### Description: 
This endpoint allows users to log in and receive an authentication token.

#### Request Body:
```bash
{
  "username": "testuser",
  "password": "testpass123"
}

````

#### Response(Success (201)):
```bash

{
  "success": true,
  "user_id": 2,
  "message": "Login successful",
  "token": "3a9333fffc9487c7076ec470269783840edc0082"
}

````
#### Response(Error (401)):
```bash

{
  "error": "Invalid credentials",
  "success": false
}

````



## Login with Google(Impotant!)

#### Endpoints
```http
POST /api/google/oauth/config/
```

#### Description: 
This give us google client and secret id which, we can use to call the googleAuthUrl.

#### Response(Success (201)):
```bash

{
  "google_client_id": "{Client Id}",
  "google_callback_uri": "{secret Id}"
}
```

#### googleAuthUrl:
```bash
https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=${googleCallbackUri}&prompt=consent&response_type=code&client_id=${googleClientId}&scope=openid%20email%20profile&access_type=offline

````
#### Description: 
Basically this googleAuthUrl give us the response of user details


#### Response(Success (201)):
```bash

{
    "success": true,
    "user_id": 6,
    "message": "Login successful",
    "token": "c7782c101dbbc13d10788b6ba570dfce6ac13653"
}

````
#### Response(Error (400)):
```bash

{
  "error": "Validation failed"
}

````

## User Management Endpoints

## Get User List

#### Endpoints
```http
GET /api/users/list/
```

#### Description: 
Retrieve a list of all registered users.

#### Response(Success (201)):
```bash

  {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": null,
    "last_name": null,
    "healthCareName": "Test Clinic",
    "address": "123 Street, City",
    "phone": "1234567890"
  }

````
#### Response(Error (400)):
```bash

{
  "error": "Validation failed"
}

````



## Get Specific User by ID

#### Endpoints
```http
GET /api/users/list/{user_id}/
```

#### Description: 
Retrieve details of a specific user by their ID.

#### Response(Success (201)):
```bash

{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": null,
  "last_name": null,
  "healthCareName": "Test Clinic",
  "address": "123 Street, City",
  "phone": "1234567890"
}


````
#### Response(Error (400)):
```bash

{
  "error": "Validation failed"
}

````

## Form Management Endpoints
## List All Forms
#### Endpoints
```http
GET /api/form/list/
```

#### Description: 
Retrieve a list of all available forms.

#### Response(Success (201)):
```bash
  {
    "id": 1,
    "creator_name": "testuser",
    "title": "test",
    "description": "test",
    "image": "http://localhost:8000/media/images/Screenshot_2024-12-20_010323.png",
    "fields": {
      "type": "text",
      "name": "first_name",
      "label": "First Name",
      "placeholder": "Enter your first name",
      "required": true,
      "max_length": 100
    },
    "is_active": true,
    "created_at": "2025-03-25T21:53:03.858475Z",
    "updated_at": "2025-03-25T21:53:03.858475Z",
    "unique_token": "2d662899-b693-4726-bd98-f8f9c22ba4bd",
    "created_by": 2
  }

````
#### Response(Error (400)):
```bash

{
  "error": "Validation failed"
}

````

## Create New Form

#### Endpoints
```http
POST /api/form/list/
```

#### Description: 
Create a new form by submitting the necessary data. Impotant matter is json field must be backend need array of json fields

#### Request Body:
```bash
{
  "title": "Survey Form",
  "description": "This form collects feedback from users.",
  "image": null,
  "fields": [
    {
      "field_name": "Name",
      "field_type": "text",
      "is_required": true
    },
    {
      "field_name": "Email",
      "field_type": "email",
      "is_required": true
    },
    {
      "field_name": "Feedback",
      "field_type": "textarea",
      "is_required": false
    }
  ],
  "is_active": true,
  "created_by": 1
}

````

#### Response(Success (201)):
```bash

{
  "success": true,
  "form_link": "http://127.0.0.1:800/api/form/dd6cc8ee-70e3-4910-b755-eda27d57485a",
  "message": "Form created successfully"
}

````
#### Response(Error (400)):
```bash

{
  "error": "Validation failed"
}

````


## Get Specific Form by ID

#### Endpoints
```http
GET /api/form/list/{form_id}/
```
### Get Forms with Query Parameters

#### Endpoints
```http
GET /api/form/list/?title=&created_by=
```

#### Description: 
In the above we use filtering form by using Query Parameters.
#### title: Filter forms by their title.
#### created_by: Filter forms by the ID of the user who created them.



## Submit a Response to a Form

#### Endpoints(NB: Here we use a link)
```http
  "form_link": "http://127.0.0.1:800/api/form/dd6cc8ee-70e3-4910-b755-eda27d57485a",
```

#### Description: 
When a admin create form and submit response successfully. He got a Unique form Link (above link), Which can share with users who can submit response through this link.




### Get All Responses Submitted by a User

#### Endpoints
```http
GET /api/form/response/
```

#### Description: 
Retrieve all form response submit by the user

#### Response(Success (201)):
```bash

[
  {
    "id": 9,
    "responder_email": "t6907169@gmail.com",
    "response_data": {
      "full_name": "Tanjid Nafis",
      "email": "t6907169@gmail.com",
      "password": "123456",
      "phone": "1626681291",
      "dob": "2025-03-20",
      "gender": "Male",
      "skills": "Python",
      "experience": "1",
      "resume": null,
      "linkedin": "https://github.com/nafijur-rahaman",
      "country": "USA",
      "bio": "nafi",
      "availability": "19",
      "user_id": "12345"
    },
    "created_at": "2025-03-27T17:32:37.853812Z",
    "updated_at": "2025-03-27T17:32:37.853812Z",
    "form": 4
  }
]



````


### Getspecefic Responses by User ID

#### Endpoints
```http
GET /api/form/response/{user_id}/
```
### Get Responses by Form and Responder Email

#### Endpoints
```http
GET /api/form/response/?form={form_id}&responder_email={email}
```

#### Description: 
In the above we use filtering response of form response.For use this filtering we get our desired form resonse.





## Support

For support, 
email tanjidnafis@gmail.com
Whatsapp: 01626681921


