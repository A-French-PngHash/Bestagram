# Bestagram API Documentation
This document provide a **full documentation** of the API used in the *Bestagram* project. It is updated as soon as new functionality are added.

# Errors
Let's begin with annoying things. When there is an error, the first field of the answer will always be named "error" and it's value will be the explanation. Error codes can also be used to determine the error.

# Login
## GET
Return the token of a user. These parameters need to be provided : 
 - username - name the user want to have
 - hash - encrypted password
 
Possible errors are : 
 - "Missing information" code 400
 - "Invalid Credentials" code 401

If operation successful, will send back something similar to : 

    {"token" : "x"} - 200

## PUT
Register a user into the database and return the token. These parameters need to be provided : 
 - username - name the user want to have
 - hash - encrypted password

Possible errors are : 
 - "Missing information" code 400
 - "Username already taken" code 409

If operation successful, will send back something similar to : 

    {"token" : "x"} - 201
