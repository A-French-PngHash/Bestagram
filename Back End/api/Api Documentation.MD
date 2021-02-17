

# Bestagram API Documentation  
This document provides a **full documentation** of the API used in the *Bestagram* project. It is updated as soon as new functionality are added.  
  
# Metadata and Errors  
In all responses you will find a "success" field. It is a bool which describe the success of the operation. 

Status code used by the api : 
|Code|Meaning|
|--|--|
| 400/500 | Error while processing query |
| 404 | Can't find resource |
| 200 | Operation succeeded |

To reduce confusion this API doesnt make use of all the HTTP status code, only these four.

In **case of an error**, more information will be provided. There will be two **additional fields** : 

 - errorCode
 - message

The error code is a code referencing to a **unique** error **for this api only**. You can find what code correspond to what error just below.
The message is a little bit of text which describe the error. It can be displayed to the user or help a programmer to identify quickly an error without having to look at the error code.

**Example** : 

    {
        "success": false,
        "errorCode": 1,
        "message": "Invalid credentials"
    }

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
| 9 | User already followed |

# Endpoints
|Title| Path | Use |  Auth  |
|--|--|--|--|
|[Login](#login)|`POST /user/login/<username>`|Login a user.|NO|
|[Register](#register)|`PUT /user/login/<username>`|Register a user.|NO|
|[Refresh Login](#refresh_login)|`POST /user/login/refresh/<refresh_token>`|Login a user.|NO
|[Search](#search_user)|`GET /user/search`|Search for users|YES|
|[Follow](#follow)|`POST /user/<id>/follow`|Follow a user|YES|
|[Post](#post)|`PUT /user/post`|Post an image|YES|
|[Email Taken](#email_taken)|`GET /email/<email>/taken`|Check if an email is taken|NO|


  
# Login
## POST  <a name="login"></a>
Return the token of a user and the refresh token. Must only be used when the client doesn't already have the refresh token. If it does have the refresh token, use the [refresh method](#login_refresh).

**Path** : `POST /user/login/<username>` 
 
  
**Query data** : 
|Name|Description|Location|Required
|--|--|--|--|
| hash | Encrypted password. Must be encrypted according to the recommendations in the global Readme for maximum security. |Parameters|YES

**Success response** :  
  
    {"success" : true, "token" : "x", "refresh_token" : "x", "token_expiration_date" : "y-M-d HH:mm:ss"} - 200
    
## PUT <a name="register"></a>
Register a user into the database and return the token.   

**Path** : `PUT /user/login/<username>`
  
**Query data** : 
|Name|Description|Location|Required
|--|--|--|--|
|hash| Encrypted password.|Parameters| YES
|email| Email associated to the account.|Parameters| YES
  
**Success response** :  
  
    {"success" : true, "token" : "x", "refresh_token" : "x", "token_expiration_date" : "y-M-d HH:mm:ss"} - 200
    
# Login - Refresh
## Post <a name="refresh_login"></a>
Return the token of a user. This method is to be used when the client already possess the refresh token, otherwise use [login](#login)

**Path** : `POST /user/login/refresh/<refresh_token>` 

**Success response** : 

    {"success" : true, "token" : "x", "token_expiration_date" : "y-M-d HH:mm:ss"}

# Email  
## Get  <a name="email_taken"></a>
Check if an email is already taken by someone.   

  **Path** : `GET /email/<email>/taken`
  
**Success response** :  
  
    {"success" : true, "taken" : true} - 200  
# Post  
## Post  <a name="post"></a>
  Create a post with an image, caption, tags...
  **Path** : `POST /user/post`

**Query data** : 
|Name|Description|Location|Required
|--|--|--|--|
|Authorization| Token of the user. | Headers | YES
|image|Image of the post.|Files| YES
|caption|Caption of the post|Parameters| YES
|tag|Contains the tags for this post in a json string. The tag information include the username of the tagged user. It also includes the position of the tag **relative to the top left corner of the image**. The position is stored into two float element, pos_x and pos_y. Both are numbers between 1 and 0. To get the true coordinate multiply pos_x by width and pos_y by height. Note that if multiple tags are sent with the same person tagged, the api will only store one of them and discard the others.  |Parameters|NO


An example of a **valid tag json** is :   
     
    { "0" :   
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
 
  
**Success response** :  
  
    {"success": True} - 200 
# Search  
## Get  <a name="search_user"></a>
Search for a user using a string. Note that the string will be matched against user's **names** and not user's username. Authentication is required as the results may vary depending on the user's searching. Returns **usernames** of the user matching the search.  

**Path** : `GET /user/search`

 **Query data** : 
|Name|Description|Location|Required
|--|--|--|--|
|Authorization|Token of the user|Header|YES
|search|Search string to be matched. If not provided then the API assume that the search is an empty string.|Parameters|NO
|offset|Offset to get values from. Begin at 0 which is the most matching result.|Parameters|YES
|row_count|Number of results to retrieve. Must be **less than a 100**.|Parameters|YES

**Success response** :  
  
    {
        "result": {
            "3": {
                "id": 18,
                "username": "onusername",
                "name": "john fries"
            },
            "4": {
                "id": 14,
                "username": "anotherusername",
                "name" : "titouan"
            },
            "5": {
                "id": 9,
                "username": "bill.gates",
                "name": "bill gates"
            }
        },
        "success": true
    }


This is an example response when offset is set to 3 and row_count to 3.

# Follow
## Post <a name="follow"></a>
Follow an other user.

**Path** : `POST /user/<id>/follow`

|Name|Description|Location|Required
|--|--|--|--|
|Authorization|Token of the user|Headers|YES

**Success response** :  

    {"success": True} - 200
