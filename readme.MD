
# Bestagram

This is a big project that I'm starting. It will consist of recreating a working copy of the well known Instagram app from Facebook. It will go from the front end which will be in a first time, a swift application for iOS to the back end, written in python. The database will be a MySQL Database.
It is an educational purpose project which mean it is not to be used in any other way than this.

You can find the **Roadmap** on [Trello](https://trello.com/b/oTma0uAS)

Here is what is discussed in this readme : 
- [Installation](#installation)
 - [Dependencies](#dependencies)
     - [Front end](#frontend)
     - [Back end](#backend)
 - [Differences with Instagram](#differences)
 - [Cryptography](#cryptography)
 - [Notes](#notes)


## API
You can find the API documentation in [Back End/api/Api Documentation](<Back End/api/Api Documentation.MD>)

## Database
You can find the database documentation in [Back End/database/Database Documentation](<Back End/database/Database Documentation.MD>)

## Installation
This is a guide on how to install Bestagram on your machine.
### Dependencies
First you will need to install the dependencies requirements of for the project. You can refer to the dependencies section right under this guide.
### Database
Once you have your dependencies installed you will **need** to setup your **MySQL database** on your local machine (or a VPS if you want). 
First install mysql-server on your machine (there are guides you can find on the internet).
Once this is done, you will find all the SQL code to create the database in `Back End/database/database.sql` You can then copy and paste everything in your open MySQL terminal.
**WARNING** : These instructions delete the database called **Bestagram** if it exists. Make sure you don't have a database named like that to prevent data loss. If you do, you can always change the database name in the SQL file (there will also be one more change to do if you do that, I will come back to it).

### Config
This is how you can configure the project. 
To allow the backend to connect to the database head towards `Back End/database/database_credentials.py`. 
The variables inside define the connection to the database. Set the value to match your local connection identifiers. **Don't track that file.**

Then you can find other configuration variables in `Back End/config.py`. However, **don't modify those variables without reasons**. They were set a those values for some reason, you need a valid reason to change it (may it be security, more user friendlier...)

This development version is intended to run on host 0.0.0.0 port 5002 (0.0.0.0:5002). **Don't change that value**. If you **have** to change it, make sure to **revert it before pushing**. If you do change it, the front end won't be able to find the server any more. You will need to head to `Front End/Bestagram/Bestagram/Model/Requests/Api.swift`. There you can change the "path" variable. If you also changed the IP address, you will need to update it in the "manager" variable.
Again, **REVERT ALL THOSE CHANGES BEFORE PUSHING**.

## Dependencies
<a name="dependencies"></a>
### Front End
<a name="frontend"></a>
The front end has two dependencies : [AlamofireImage](https://github.com/Alamofire/AlamofireImage) and [Cache](https://github.com/hyperoslo/Cache). Both of these dependencies can be installed via CocoaPods. After installing CocoaPods, just run  :

    pod install
   
in the directory where you have your .xcodeproj and you will be all set. Don't forget to open the .xcworkspace from now on to include the dependencies.

### Back end
<a name="backend"></a>
Backend dependencies are written in the requirements.txt files. You can find this file in the following directory : 
`Back End/requirements.txt`
Dependencies are : 

 - [Flask](https://pypi.org/project/Flask/)
 - [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
 - [requests](https://pypi.org/project/requests/)
 - [Pillow](https://pypi.org/project/Pillow/)

You can install them through **pip** : 

    pip -r requirements.txt


## Differences from the original Instagram app
<a name="differences"></a>

There is a few differences from the original Instagram app that I will explain here.

There will be **no Explore tab**, as I want to make this copy more friends for friends. Moreover, to give an Explore tab, Facebook uses complex machine learning which would take years to implement.

In a first approach the posts will consist of a single image.

## Cryptography
<a name="cryptography"></a>

This is an important part of this readme. This describes the security protocol set up in order to provide full end to end security. 
When a user inputs its password, it is hashed on the client side. The hashing algorithm used is **pbkdf2** using the **Hmac algorithm SHA-256**. The derived key length must be **32 bytes**. **1 000 000** iterations must be performed. The salt must be the **username encoded in utf-8**. Because the username is unique, it serves the purpose of a salt. The hashed version is then converted to hexadecimal.

The hashed password is then securely transmitted over an SSL connection. This hashed version is the version to protect.

When it arrives at the server side, it must be hashed again in order to protect the previously hashed version. Because the client did 1 000 000 iterations on it, we can limit the server side iterations to **10 000**. The algorithm is the same : **pbkdf2** using the **Hmac algorithm SHA-256**. Derived key is again **32 bytes** and salt is the **username encoded in utf-8**.

If this protocol is followed the user's password and user's hashed password (client side version) are never revealed.

## Notes
 <a name="notes"></a>

While creating the app I'm trying to use as much SF Symbol as possible in order to limit the number of assets to import.
