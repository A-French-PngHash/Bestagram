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
struct User {
    var username: String = ""
    /// Number of followers of this users.
    var followers: Int = -1
    var numberOfPosts: Int = -1
    var profilePicture: UIImage! = nil
    /// Actual token for this user.
    var token: String

    /// Temporary init. No api call is done at the moment (as there is no api implemented) so for testing purposes,
    /// data is created manually.
    init(username: String, followers: Int, numberOfPosts: Int, profilePicture: UIImage) {
        self.username = username
        self.followers = followers
        self.numberOfPosts = numberOfPosts
        self.profilePicture = profilePicture
        self.token = ""
    }

    /// This init will login the user with the provided data. It will load the token for further request.
    ///
    /// - parameter username: Username or email used for connection.
    /// - parameter password: The unencrypted password used to connect.
    /// - Parameters:
    ///     - loadingFinished: Closure called when the token has finished being loaded from the API.
    ///     -  success: Wether the fetch succeeded or not.
    ///     - error: If the request was not succesful then this is the error corresponding to the fail.
    init(username: String, password : String, loadingFinished : @escaping (_ success: Bool, _ error: BestagramError?) -> Void) {
        self.username = username

        // Hashing the password as described in the API documentation.
        let salt = password.data(using: .utf8)!
        let hash = Hashing.shared.toHex(Hashing.shared.pbkdf2(hash: CCPBKDFAlgorithm(kCCPRFHmacAlgSHA256), password: password, saltData: salt, keyByteCount: 64, rounds: 1000000)!)

        LoginService.shared.fetchToken(username: username, password: hash) { (success, content, code) in
            guard success && code == 200 else{
                if code == 401 {
                    // Invalid credentials.
                    loadingFinished(false, InvalidCredentials())
                } else if code == 400 {
                    // Missing informations.
                    loadingFinished(false, MissingInformations())
                } else {
                    // Unknown error.
                    loadingFinished(false, UnknownError(documentation: content))
                }
                return
            }
            // Load of the token was succesfull.
            loadingFinished(true, nil)
        }
        self.token = ""
    }
}
