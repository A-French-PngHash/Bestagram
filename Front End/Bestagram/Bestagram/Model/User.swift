//
//  User.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/11/2020.
//

import UIKit

/// Represent a user of the app.
struct User {
    var username: String = ""
    /// Number of followers of this users.
    var followers: Int = 0
    var numberOfPosts: Int = 0
    var profilePicture: UIImage! = nil

    /// Temporary init. No api call is done at the moment (as there is no api implemented) so for testing purposes,
    /// data is created manually.
    init(username: String, followers: Int, numberOfPosts: Int, profilePicture: UIImage) {
        self.username = username
        self.followers = followers
        self.numberOfPosts = numberOfPosts
        self.profilePicture = profilePicture
    }

    /// This init will login the user with the provided data. It will load the token for further request.
    ///
    /// - parameter username: Username or email used for connection.
    /// - parameter password: The unencrypted password used to connect.
    init(username: String, password : String) {

    }
}
