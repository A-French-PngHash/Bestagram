//
//  CredentialService.swift
//  Bestagram
//
//  Created by Titouan Blossier on 23/01/2021.
//

import Foundation

/// Store and retrieve refresh token(s) from the local storage.
///
/// Note that currently this class only store a refresh token for one user. This may change in the future with the possibility of having multiple different account connected.
class CredentialService {
    static let shared = CredentialService()
    private init() { }

    let defaults = UserDefaults.standard

    /// Store the refresh token in user defaults.
    ///
    /// - parameter refreshToken: Refresh token.
    ///
    func store(refreshToken: String) {
        defaults.set(refreshToken, forKey: "refreshToken")
    }

    /// Retrieve stored credentials from user default.
    ///
    /// - returns : The refresh token.
    func get() -> String{
        return defaults.string(forKey: "refreshToken")!
    }
}
