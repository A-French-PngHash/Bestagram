
  
# Bestagram API Documentation  
This document provides a **full documentation** of the API used in the *Bestagram* project. It is updated as soon as new functionality are added.  
  
# Metadata and Errors  
In all responses you will find a "success" field. It is a bool which describe the success of the operation. The HTTP status code will be to 400/500 if the operation didn't succeed and it will be 200 if it did. To reduce confusion this API doesnt make use of all the HTTP status code, only these three.

In **case of an error**, more information will be provided. There will be two **additional fields** : 

 - errorCode
 - message

The error code is a code referencing to a **unique** error **for this api only**. You can find what code correspond to what error just below.
The message is a little bit of text which describe the error. It can be displayed to the user or help a programmer to identify quickly an error without having to look at the error code.

## Error codes
The following table maps each error code the API can possibly raise.
|Code| Error |
|--|--|
| 1 | Invalid credentials |
| 2 | Username taken |
| 3 | Email taken |
| 4 | Invalid email |
| 5 | Invalid username |
| 6 | Invalid name |
| 7 | Missing information |
| 8 | Username not existing |


  
# Login  
## GET  
  
 GET /login  Return the token of a user.   
  
Query Parameters :   
 - username : name the user want to have.  
 - hash : an encrypted password.  
  
Response if operation successful :  
  
	{"token" : "x", "token_expiration_date": "2021-01-25 00:21:00"} - 200  
## PUT  
 PUT /login  Register a user into the database and return the token.   
  
Query parameters :  
 - username : name the user want to have.  
 - hash : an encrypted password.  
 - email : email associated to the account.   
  
Response if operation successful :  
  
	{"token" : "x", "token_expiration_date": "2021-01-25 16:00:01"} - 201  
# Email  
## Get  
  
 GET /email  Check if an email is already taken by someone.   
  
Query parameters :  
 - email : The email to check for.  
  
Response if operation successful :  
  
	{"taken" : true} - 200  
# Post  
## Post  
  
 POST /post  Create a post with an image, caption...  
  
Headers :  
 - Authorization : Token of the user.  
  
Query parameters :  
 - caption : Caption of the post.  
 - tag : The tag parameters is **not mandatory**. It contains the tags for this post in a json string.   
The tag information include the username of the tagged user. It also includes the position of the tag **relative to the bottom left corner of the image**. The position is stored into two float element, pos_x and pos_y. Both are numbers between 1 and 0. To get the true coordinate multiply pos_x by width and pos_y by height. Note that if multiple tags are sent with the same person tagged, the api will only store one of them and discard the others.  
  
An example of a valid json body is :   
     
	 {      "tags" :   
	      {   
	         "0" :   
	         {   
	            "pos_x" : 0.43,   
	            "pox_y" : 0.87,   
	            "username" : "john.fries"  
	 },         "1" :   
	         {    
	            "pos_x" : 0.29,   
	            "pos_y" : 0.44,   
	            "username" : "titouan"   
	         }  
	 } }  
  
Files :   
 - image : The image of the post.  
  
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

  
Response if operation successful :  
  
	 {3: "usernamematched", 4: "anotherusername", 5: "athirdusername"}  
This is an example response when offset is set to 3 and row_count to 3.
