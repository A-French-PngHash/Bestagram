
# Bestagram API Documentation
This document provides a **full documentation** of the API used in the *Bestagram* project. It is updated as soon as new functionality are added.

# Errors
When there is an error, the first field of the answer will always be named "error", and it's value will be the explanation. Error codes can also be used to determine the error.

# Login
## GET

    GET /login
   
Return the token of a user. 

Query Parameters : 
 - username : name the user want to have.
 - hash : an encrypted password.
 
Errors : 
 - "Missing information" code **400**.
 - "Invalid Credentials" code **401**.

Response if operation successful :

    {"token" : "x"} - 200

## PUT
    PUT /login
   
Register a user into the database and return the token. 

Query parameters :
 - username : name the user want to have.
 - hash : an encrypted password.
 - email : email associated to the account.

Errors : 
 - "Missing information" code **400**.
 - "Username already taken" code **409**.
 - "Email already taken" code **409**.
 - "Invalid email" code **406**.
 - "Invalid username" code **406**.

Response if operation successful :

    {"token" : "x"} - 201

# Email
## Get

    GET /email
   
Check if an email is already taken by someone. 

Query parameters :
 - email : The email to check for.

Errors :
 - "Missing information" code **400**.

Response if operation successful :

    {"taken" : true} - 200

# Post
## Post

    POST /post
   
Create a post with an image, caption...

Headers :
 - Authorization : Token of the user.

Query parameters :
 - caption : Caption of the post.
 - tag : The tag parameters is **not mandatory**. It contains the tags for this post in a json string. 
The tag information include the username of the tagged user. It also includes the position of the tag **relative to the bottom left corner of the image**. The position is stored into two float element, pos_x and pos_y. Both are numbers between 1 and 0. To get the true coordinate multiply pos_x by width and pos_y by height. Note that if multiple tags are sent with the same person tagged, the api will only store one of them and discard the others.

An example of a valid json body is : 
	
	{  
		"tags" : 
		{ 
			"0" : 
			{ 
				"pos_x" : 0.43, 
				"pox_y" : 0.87, 
				"username" : "john.fries"
			}, 
			"1" : 
			{ 	
				"pos_x" : 0.29, 
				"pos_y" : 0.44, 
				"username" : "titouan" 
			}
		}
	}


Files : 
 - image : The image of the post.

Errors :
 - "Missing Information" code **400**.
 - "Invalid credentials" code **401**.

Response if operation successful :

    {"status": "Image Received"}, 201

# Search
## Get

    GET /search

Search for a user using a string. Note that the string will be matched against user's **names** and not user's username. Authentication is required as the results may vary depending on the user's searching. Returns **usernames** of the user matching the search.

Headers :
- Authorization : Token of the user.

Query parameters : 
- search : Search string to be matched. **Optional** parameter, if not provided then the API assume that the search is an empty string.
- offset : Offset to get values from. Begin at 0 which is the most matching result.
- row_count : Number of results to retrieve. Must be **less than a 100**.

Errors : 
 - "Missing Information" code **400**.
 - "Invalid credentials" code **401**.

Response if operation successful :

    {3: "usernamematched", 4: "anotherusername", 5: "athirdusername"}
  This is an example response when offset is set to 3 and row_count to 3.
