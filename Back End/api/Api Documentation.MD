
# Bestagram API Documentation
This document provide a **full documentation** of the API used in the *Bestagram* project. It is updated as soon as new functionality are added.

# Errors
When there is an error, the first field of the answer will always be named "error" and it's value will be the explanation. Error codes can also be used to determine the error.

# Login
## GET
Return the token of a user. 

Parameters : 
 - username : name the user want to have.
 - hash : encrypted password.
 
Errors : 
 - "Missing information" code **400**.
 - "Invalid Credentials" code **401**.

Response if operation successful :

    {"token" : "x"} - 200

## PUT
Register a user into the database and return the token. 

Parameters :
 - username : name the user want to have.
 - hash : encrypted password.
 - email : email associated to the account.

Errors : 
 - "Missing information" code **400**.
 - "Username already taken" code **409**.
 - "Email already taken" code **409**.

Response if operation successful :

    {"token" : "x"} - 201

# Email
## Get
Check if an email is already taken by someone. 

Parameters : 
 - email : The email to check for.

Errors :
 - "Missing information" code **400**.

Response if operation successful :

    {"taken" : true} - 200

# Post
## Post
Create a post with an image, description...
Headers :
 - Authorization : Token of the user.
 - Username : Username of the user who is making the post.

Parameters :
 - image : The image of the post.
 - description : Description of the post.

Errors :
 - "Missing Information" code **400**.
 - "Invalid credentials" code **401**

Response if operation successful :

    {"status": "Image Received"}, 201
