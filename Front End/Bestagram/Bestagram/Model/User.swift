//
//  User.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/11/2020.
//

import UIKit
import CommonCrypto

/// Represent a user of the app.
///
/// When properties are by default initialized at -1 or "", it means that their value have not yet been fetched from the server.
class User {
    /// Name of the user. e.g. "Jon Appleseed"
    var name: String?
    /// Username of the user. e.g. "jon.apple"
    var username: String?
    /// Number of followers of this users.
    var followers: Int = -1
    var numberOfPosts: Int = -1
    var profilePicture: UIImage! = nil
    var email : String?
    var hash: String?
    /// Wether or not the credentials have previously been saved in user default and can be accessible at any time.
    var credentialsSaved: Bool?

    /// Temporary init. No api call is done at the moment (as there is no api implemented) so for testing purposes,
    /// data is created manually.
    init(username: String, followers: Int, numberOfPosts: Int, profilePicture: UIImage) {
        self.username = username
        self.followers = followers
        self.numberOfPosts = numberOfPosts
        self.profilePicture = profilePicture
        self.email = ""
        self.hash = ""
    }

    /// This init login a user. It fill this class credentials variable to allow this class to be used in different actions after that can only be done by this user.
    ///
    /// - parameter credentialsSaved: Wether or not the credentials have been saved in the CredentialService
    /// - parameter username: If the credentials are not saved, this is the username.
    /// - parameter password: If the credentials are not saved this is the password **non hashed**.
    /// - parameter saveCredentials: If the credentials are not saved yet this init can save them in the CredentialService for easier and persistent access.
    init(credentialsSaved: Bool, username: String?, password: String?, saveCredentials: Bool?) {
        if credentialsSaved {
            self.credentialsSaved = true
            let credentials = CredentialService.shared.get()
            if let username = credentials["username"], let hash = credentials["password"] {
                self.username = username
                self.hash = hash
            }
        } else {
            if let username = username, let password = password{
                let hash = Hashing.shared.hash(password: password, salt: username)
                self.username = username
                self.hash = hash
                if let save = saveCredentials, save {
                    CredentialService.shared.store(password: hash, username: username)
                }
            }
        }
    }

    /// Retrieve token for this user. This method only works if the credentials variable have been filled.
    func getToken(callback: @escaping (_ success: Bool, _ token: String?, _ error: BestagramError?) -> Void) {
        let token = try? CacheStorage.shared.storage.object(forKey: "token")

        if token == nil || ((try? CacheStorage.shared.storage.isExpiredObject(forKey: "token")) == true){
            // Token has never been retrieved.
            if let username = self.username, let hash = self.hash {
                LoginService.shared.fetchToken(username: username, password: hash, register: false) { (success, token, expirationDate, error) in
                    guard let token = token, let expirationDate = expirationDate, success else {
                        callback(false, nil, error)
                        return
                    }
                    do{
                        try CacheStorage.shared.storage.setObject(token, forKey: "token", expiry: .date(expirationDate))
                    } catch {
                        print(error)
                    }
                    callback(success, token, error)
                }
            } else {
                callback(false, nil, BestagramError.InvalidCredentials)
            }
        } else {
            // Token has been retrieved.
            callback(true, token, nil)
        }
    }

    /// This static function create a user.
    ///
    /// - parameter username: Username or email used for connection.
    /// - parameter password: The unencrypted password used to connect.
    /// - parameter email: Email of the user. Required only in case of a sign up.
    /// - parameter save: Save credentials in local storage. By default set to true.
    /// - Parameters:
    ///     - callback: Closure called when the token has finished being loaded from the API.
    ///     - success: Wether the fetch succeeded or not.
    ///     - error: If the request was not succesful then this is the error corresponding to the fail.
    static func create(username: String, password: String, email: String, name: String, save: Bool = true, callback: @escaping (_ success: Bool, _ error: BestagramError?) -> Void){
        let hash = Hashing.shared.hash(password: password, salt: username)

        LoginService.shared.fetchToken(username: username, password: hash, email : email, register: true, name: name) { (success, token, tokenExpirationDate, error) in
            if success, save {
                CredentialService.shared.store(password: hash, username: username)
            }
            callback(success, error)
        }
    }
}
