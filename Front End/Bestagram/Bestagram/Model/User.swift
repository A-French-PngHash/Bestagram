//
//  User.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/11/2020.
//

import UIKit

/// Represent a user of the app.
struct User {
    var username: String
    /// Number of followers of this users.
    var followers: Int
    var numberOfPosts: Int
    var profilePicture: UIImage

    /// Temporary init. No api call is done at the moment (as there is no api implemented) so for testing purposes,
    /// data is created manually.
    init(username: String, followers: Int, numberOfPosts: Int, profilePicture: UIImage) {
        self.username = username
        self.followers = followers
        self.numberOfPosts = numberOfPosts
        self.profilePicture = profilePicture
    }
}
