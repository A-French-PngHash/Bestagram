//
//  Tag.swift
//  Bestagram
//
//  Created by Titouan Blossier on 01/01/2021.
//

import UIKit

/// Represent one tag on a post.
class Tag {
    var userTagged: User
    /// Position of the tag on the picture. Two numbers between 1 and 0.
    var position: Array<Float>

    /// This init fetch the tags from a post using the api.
    init(post: Post) {
        //TODO: - Fetch data from api
        userTagged = User(username: "test", followers: 1, numberOfPosts: 1, profilePicture: UIImage())
        position = [0, 0]
    }

    /// This init create a tag locally. The tag can later be sent to the api.
    init(userTagged: User, position: Array<Float>) {
        self.userTagged = userTagged
        self.position = position
    }
}
