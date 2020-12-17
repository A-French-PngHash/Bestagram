# Bestagram

This is a big project that I'm starting. It will consist of recreating a working copy of the well known Instagram app from Facebook. It will goes from the front end which will be in a first time, a swift application for Ios to the back end, written in python. The database will be a MySQL Database.
It is an educationnal purpose project which mean it is not to be used in any other way than this.

You can find the **Roadmap** on [Trello](https://trello.com/b/oTma0uAS)

## API
You can find the API documentation in "Back End/api/Api Documentation.MD".
The API uses a self signed root certificate and a certificate issued by the root certificate. To allow everything to work as intended, you will need to install the root certificate on your machine. You can find it in "Back End/ApiCertificate/rootCA.crt". Doubleclick on it to install it. Then search for it in the keychain, double click on it, open the trust section and allow full trust by changing "When using this certificate" from "Use sytem defaults" to "Always trust".
Note that this step is really required if you want to work on the front end. As I found no way to allow the use of self signed certificate in the IOS app, I was forced to use a root certificate. If you are developping the back end, you shouldn't need it as api testing have options to allow self signed certificates.

## Dependencies
### Front End
The front end has two dependencies : [AlamofireImage](https://github.com/Alamofire/AlamofireImage) and [Cache](https://github.com/hyperoslo/Cache). Both of this dependencies can be easily installed via CocoaPods. After installing CocoaPods, just run :

    pod install
   
in the folder where you find the .xcodeproj and you will be all set. Don't forget to open the .xcworkspace from now on to include the dependencies.


## Differences from the original Instagram app

There is a few differences from the original Instagram app that I will explain here.

There will be **no Explore tab**, as I want to make this copy more friends for friends. Moreover, to give an Explore tab, Facebook uses very complex machine learning which would take years to implement.

## Notes
 
While creating the app I'm trying to use as much SF Symbol as possible in order to limit the number of assets to import.
