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
    var username: String = ""
    /// Number of followers of this users.
    var followers: Int = -1
    var numberOfPosts: Int = -1
    var profilePicture: UIImage! = nil
    /// Actual token for this user.
    var token: String
    var email : String
    var hash: String

    /// Temporary init. No api call is done at the moment (as there is no api implemented) so for testing purposes,
    /// data is created manually.
    init(username: String, followers: Int, numberOfPosts: Int, profilePicture: UIImage) {
        self.username = username
        self.followers = followers
        self.numberOfPosts = numberOfPosts
        self.profilePicture = profilePicture
        self.token = ""
        self.email = ""
        self.hash = ""
    }

    /// This init will login/register the user with the provided data. It will load the token for further request.
    ///
    /// - parameter username: Username or email used for connection.
    /// - parameter password: The unencrypted password used to connect.
    /// - parameter email: Email of the user. Required only in case of a sign up.
    /// - parameter register: If this parameter is set to true then the programm will send a register querry.
    /// - Parameters:
    ///     - loadingFinished: Closure called when the token has finished being loaded from the API.
    ///     - success: Wether the fetch succeeded or not.
    ///     - error: If the request was not succesful then this is the error corresponding to the fail.
    init(username: String, password: String, email: String = "", register: Bool = false, name: String?, loadingFinished : @escaping (_ success: Bool, _ error: BestagramError?) -> Void) {
        self.username = username
        self.email = email
        if let n = name {
            self.name = n
        }

        // Hashing the password as described in the global readme.
        let salt = username.data(using: .utf8)!
        let hash = Hashing.shared.toHex(Hashing.shared.pbkdf2(hash: CCPBKDFAlgorithm(kCCPRFHmacAlgSHA256), password: password, saltData: salt, keyByteCount: 32, rounds: 1000000)!)
        self.hash = hash
        self.token = ""

        if register {
            LoginService.shared.fetchToken(username: self.username, password: hash, email : email, register: true) { (success, content, code) in
                if success {
                    self.token = content!
                }
                let errorResponse = User.interpretResponse(success: success, code: code, content: content)
                loadingFinished(errorResponse.0, errorResponse.1)
            }
        } else {
            LoginService.shared.fetchToken(username: username, password: hash, register: false) { (success, content, code) in
                if success {
                    self.token = content!
                }
                let errorResponse = User.interpretResponse(success: success, code: code, content: content)
                loadingFinished(errorResponse.0, errorResponse.1)
            }
        }
    }

    /// Interpret an API error by getting the error that is associated with it if there is one.
    ///
    /// - parameter success: Wether the request succeeded or not.
    /// - parameter code: HHTPStatusCode of the request.
    /// - parameter content: Answer of the querry. Is used to provide more information in case of an unknown error.
    static func interpretResponse(success: Bool, code : Int?, content: String?) -> (Bool, BestagramError?) {
        guard success && (code == 200 || code == 201) else{
            if code == 401 {
                // Invalid credentials.
                return (false, InvalidCredentials())
            } else if code == 400 {
                // Missing informations.
                return (false, MissingInformations())
            } else if code == 409 {
                return (false, UsernameAlreadyTaken())
            } else{
                // Unknown error.
                return (false, UnknownError(documentation: content))
            }
        }
        // Load of the token was succesfull.
        return (true, nil)
    }

    /// The default username is everything that precede the "@" in the user's email adress.
    /// This function retrieve the username. Note that the email adress must be valid and contain one @ sign.
    ///
    /// - Throws : InvalidEmailAdress
    /// - Returns : Username from the email adress.
    static func usernameFromEmail(email: String) throws -> String {
        // There should only be one @ in the email adress.
        guard let atIndex = email.firstIndex(of: "@") else {
            throw InvalidEmailAdress()
        }
        let username = email.prefix(upTo: atIndex)
        return String(username)
    }
}
