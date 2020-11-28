//
//  Post.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import UIKit

/// Represent a post made by a user of the app.
class Post {
    /// The user who posted the image.
    let user : User
    /// Image of the post.
    ///
    /// For the moment posts only consist of one image.
    let image : UIImage
    let numberOfLikes : Int
    
    init(user : User, image : UIImage, numberOfLikes : Int) {
        self.user = user
        self.image = image
        self.numberOfLikes = numberOfLikes
    }
    
}
