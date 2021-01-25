//
//  CredentialService.swift
//  Bestagram
//
//  Created by Titouan Blossier on 23/01/2021.
//

import Foundation

/// Store and retrieve credentials from the local storage. /!\ The "password" is actually the hash of the password.
///
/// Note that currently this class only store credentials for one user. This may change in the future with the possibility of having multiple different account connected.
class CredentialService {
    static let shared = CredentialService()
    private init() { }

    let defaults = UserDefaults.standard

    /// Store the given credentials in user defaults.
    ///
    /// - parameter password: Hashed password.
    /// - parameter username: Username.
    ///
    func store(password: String, username: String) {
        defaults.set(password, forKey: "password")
        defaults.set(username, forKey: "username")
    }

    /// Retrieve stored credentials from user default.
    ///
    /// - returns : Returns password and username under the key password and username.
    func get() -> Dictionary<String, String>{
        return [
            "password": defaults.string(forKey: "password")!,
            "username": defaults.string(forKey: "username")!
        ]
    }
}
