//
//  Post.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import UIKit

/// Represent a post made by a user of the app.
class Post {
    //MARK: - Static variables
    static let minimumCharacterReducedDescription : Int = 30
    
    //MARK: - Other variables
    /// The user who posted the image.
    let user : User
    /// Image of the post.
    ///
    /// For the moment posts only consist of one image.
    let image : UIImage
    let numberOfLikes : Int
    /// The full description is all the text entered by the user when they added it.
    let fullDescription : String
    /// The reduced description is what is shown to the user when they scroll through. They can decide to click on it to show the full description.
    var reducedDescription : String! = nil
    
    //MARK: - Initialization
    init(user : User, image : UIImage, numberOfLikes : Int, description : String) {
        self.user = user
        self.image = image
        self.numberOfLikes = numberOfLikes
        self.fullDescription = description
        self.reducedDescription = getReducedDescriptionFrom(description: description)
    }
    
    //MARK: - Functions
    /// Calculate and return the reduced description using certain rules.
    ///
    /// The reduced description can't cut a word in half (except if its a really big word) and has a minimum of characters.
    private func getReducedDescriptionFrom(description : String) -> String{
        var index = Post.minimumCharacterReducedDescription
        while description[index] != " " || Post.minimumCharacterReducedDescription - index >= 10 {
            index += 1
        }
        return String(description.prefix(index))
    }
    
}
