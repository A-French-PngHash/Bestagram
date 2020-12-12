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
    func getDisplayPostDateInformation() -> String {
        /// Return a string like "32 minutes ago" that is shown to the user to inform him of when this was posted.
        ///
        /// Always floor the result, for example if it's been 1 month and a half or even 1 month
        /// and three quarters it will return "1 month ago".

        let calendar = Calendar.current
        let components = calendar.dateComponents(
            [.year, .month, .day, .hour, .minute, .second],
            from: postTime,
            to: Date())
        print(components)

        if components.year != 0 {
            return makeString(value: components.year!, unit: "year")
        } else if components.month != 0 {
            return makeString(value: components.month!, unit: "month")
        } else if components.day != 0 {
            return makeString(value: components.day!, unit: "day")
        } else if components.hour != 0 {
            return makeString(value: components.hour!, unit: "hour")
        } else if components.minute != 0 {
            return makeString(value: components.minute!, unit: "minute")
        } else {
            return makeString(value: components.second!, unit: "second")
        }
    }

    private func makeString(value: Int, unit: String) -> String {
        /// Return a string like "3 months ago".
        ///
        /// - Parameter value: The number that need to precid the unit.
        /// Will also be use to calculate if an s need to be added at the end.
        ///
        /// - Parameter unit: The unit (can be year, month, second...).
        /// IMPORTANT : don't put this unit to plural, this function will set it to plural if necessary.
        if value > 1 {
            return "\(value) \(unit)s ago"
        } else {
            return "\(value) \(unit) ago"
        }

    }
}
