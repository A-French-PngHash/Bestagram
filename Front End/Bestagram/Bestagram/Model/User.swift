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
    var refreshToken : String?

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
    /// - parameter username: If the refresh token is not saved, this is the username to be used.
    /// - parameter password: If the refresh token is not saved, this is the password to be used - **must not be hashed**.
    /// - parameter saveCredentials: If the credentials are not saved yet this init can save them in the CredentialService for easier and persistent access.
    init(username: String? = "", password: String? = "", authenticationFinished: @escaping (_ success: Bool, _ token: String?, _ error: BestagramError?) -> Void) {
        if username == "" { // Authentication via refresh token.
            getToken(callback: authenticationFinished)
        } else {
            if let username = username, let password = password{
                let hash = Hashing.shared.hash(password: password, salt: username)
                getToken(username: username, hash: hash, callback: authenticationFinished)
            } else {
                fatalError("refreshTokenSaved was set to false and no username + hash was provided. Authentication impossible.")
            }
        }
    }

    func getToken(callback: @escaping (_ success: Bool, _ token: String?, _ error: BestagramError?) -> Void) {
        self.getToken(username: nil, hash: nil, callback: callback)
    }

    private func getToken(username: String?, hash: String?, callback: @escaping (_ success: Bool, _ token: String?, _ error: BestagramError?) -> Void) {
        let token = try? CacheStorage.shared.storage.object(forKey: "token")

        func processTokenResponse(success: Bool, token: String?, expirationDate: Date?, refreshToken: String?, error: BestagramError?) {
            guard  success, let token = token, let expirationDate = expirationDate else {
                callback(false, nil, error)
                return
            }
            if let refreshTok = refreshToken {
                // Storing refresh token for future use.
                CredentialService.shared.store(refreshToken: refreshTok)
            }
            do {
                try CacheStorage.shared.storage.setObject(token, forKey: "token", expiry: .date(expirationDate))
            } catch {
                print(error)
            }
            callback(success, token, error)
        }

        if token == nil || ((try? CacheStorage.shared.storage.isExpiredObject(forKey: "token")) == true){
            // Token need to be retrieved. It is either expired or has never been retrieved.
            if let username = username, let hash = hash { // Using credentials; Usually in the case of a first authentication. SHould not provided if refresh token is disponible.
                LoginService.shared.login(username: username, password: hash, callback: processTokenResponse)
            } else { // Authentication using refresh token.
                LoginService.shared.refreshLogin(refreshToken: CredentialService.shared.get(), callback: processTokenResponse)
            }
        } else {
            // Token is already stored and up to date in cache.
            callback(true, token, nil)
        }
    }

    /// This static function creates a user and save the token and refresh token of this new user.
    ///
    /// - parameter username: Username or email used for connection.
    /// - parameter password: The unencrypted password used to connect.
    /// - parameter email: Email of the user. Required only in case of a sign up.
    /// - parameter save: Save credentials in local storage. By default set to true.
    /// - Parameters:
    ///     - callback: Closure called when the token has finished being loaded from the API.
    ///     - success: Wether the fetch succeeded or not.
    ///     - error: If the request was not succesful then this is the error corresponding to the fail.
    static func create(username: String, password: String, email: String, name: String, callback: @escaping (_ success: Bool, _ error: BestagramError?) -> Void){
        let hash = Hashing.shared.hash(password: password, salt: username)

        LoginService.shared.signup(username: username, password: hash, email: email, name: name) { (success, token, expirationDate, refreshToken, error) in
            if success, let token = token, let expirationDate = expirationDate, let refreshToken = refreshToken {
                CredentialService.shared.store(refreshToken: refreshToken)
                do {
                    try CacheStorage.shared.storage.setObject(token, forKey: "token", expiry: .date(expirationDate))
                } catch {
                    print(error)
                }
            }
            callback(success, error)
        }
    }
}
