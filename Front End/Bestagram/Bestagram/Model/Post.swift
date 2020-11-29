//
//  Post.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import UIKit

/// Represent a post made by a user of the app.
class Post {
    // MARK: - Static variables
    static let minimumCharacterReducedDescription: Int = 30

    // MARK: - Other variables
    /// The user who posted the image.
    let user: User
    /// Image of the post.
    ///
    /// For the moment posts only consist of one image.
    let image: UIImage
    let numberOfLikes: Int
    let description: Description
    /// The date when the post was finished being uploaded to the server.
    let postTime: Date

    // MARK: - Initialization
    init(user: User, image: UIImage, numberOfLikes: Int, description: String, postTime: Date) {
        self.user = user
        self.image = image
        self.numberOfLikes = numberOfLikes
        self.description = Description(text: description)
        self.postTime = postTime
    }

    // MARK: - Functions
    func getDisplayPostDateInformation() {
        /// Return a string like "32 minutes ago" that is shown to the user to inform him of when this was posted.
        ///
        /// Always floor the result, for example if it's been 1 month and a half or even 1 month
        /// and three quarters it will return "1 month ago".
        print(postTime)
    }
}
