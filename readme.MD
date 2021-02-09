# Bestagram

This is a big project that I'm starting. It will consist of recreating a working copy of the well known Instagram app from Facebook. It will goes from the front end which will be in a first time, a swift application for Ios to the back end, written in python. The database will be a MySQL Database.
It is an educationnal purpose project which mean it is not to be used in any other way than this.

You can find the **Roadmap** on [Trello](https://trello.com/b/oTma0uAS)

Here is what is discussed in this readme : 
 - [Dependencies](#dependencies)
     - [Front end](#frontend)
     - [Back end](#backend)
 - [Differences with Instagram](#differences)
 - [Cryptography](#cryptography)
 - [Notes](#notes)


## API
You can find the API documentation in [Back End/api/Api Documentation](Back End/api/Api Documentation.md)"

## Database
You can find the database documenation in [Back End/database/Database Documentation](Back\ End/database/Database\ Documentation.md)

## Dependencies
<a name="dependencies"></a>
### Front End
<a name="frontend"></a>
The front end has two dependencies : [AlamofireImage](https://github.com/Alamofire/AlamofireImage) and [Cache](https://github.com/hyperoslo/Cache). Both of this dependencies can be easily installed via CocoaPods. After installing CocoaPods, just run :

    pod install
   
   in the folder where you find the .xcodeproj and you will be all set. Don't forget to open the .xcworkspace from now on to include the dependencies.

### Back end
<a name="backend"></a>
Backend dependencies are written in the requirements.txt files. They are : 

 - [Flask](https://pypi.org/project/Flask/)
 - [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
 - [requests](https://pypi.org/project/requests/)
 - [Pillow](https://pypi.org/project/Pillow/)

## Differences from the original Instagram app
<a name="differences"></a>

There is a few differences from the original Instagram app that I will explain here.

There will be **no Explore tab**, as I want to make this copy more friends for friends. Moreover, to give an Explore tab, Facebook uses very complex machine learning which would take years to implement.

In a first approach the posts will only consist of a single image.

## Cryptography
<a name="cryptography"></a>

This is an important part of this readme. This describes the security protocol set up in order to provide full end to end security. 
When a user inputs its password, it is hashed on the client side. The hashing algorithm used is **pbkdf2** using the **Hmac algorithm SHA-256**. The derived key length must be **32 bytes**. **1 000 000** iterations must be performed. The salt must be the **username encoded in utf-8**. Because the username is unique, it serves the purpose of a salt. The hashed version is then converted to hexadecimal.

The hashed password is then securely transmitted over an ssl connection. This hashed version is the version to protect.

When it arrives on the server side, it must be hashed again in order to protect the previously hashed version. Because the client side already did 1 000 000 iterations on it, we can limit the server side iterations to **10 000**. The algorithm is the same : **pbkdf2** using the **Hmac algorithm SHA-256**. Derived key is again **32 bytes** and salt is the **username encoded in utf-8**.

If this protocol is followed the user's password and user's hashed password (client side version) are never revealed.

## Notes
 <a name="notes"></a>

While creating the app I'm trying to use as much SF Symbol as possible in order to limit the number of assets to import.
