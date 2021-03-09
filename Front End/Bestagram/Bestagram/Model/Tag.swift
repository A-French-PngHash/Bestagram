//
//  Tag.swift
//  Bestagram
//
//  Created by Titouan Blossier on 01/01/2021.
//

import UIKit

/// Represent one tag on a post.
///
/// Conforl to hashable in order to iterate over list of tags in a ForEach loop.
class Tag {

    /// Username fo the user's tagged.
    var userTagged: User
    /// Position of the tag on the picture. Two numbers between 1 and 0.
    var position: Array<Float>

    /// This init fetch the tags from a post using the api.
    init(post: Post) {
        //TODO: - Fetch data from api
        userTagged = User(id: -1, username: "test", name: "test")
        position = [0, 0]
    }

    /// This init create a tag locally. The tag can later be sent to the api.
    ///
    /// - parameter userTagged: Username of the user's tagged.
    /// - parameter position: Array containing two floats. The x and y position. Both are numbers between 1 and 0. They are relative to the bottom left corner of the image.
    init(userTagged: User, position: Array<Float>) {
        self.userTagged = userTagged
        self.position = position
    }

    /// Returns json representation of this tag.
    func encodeJson() -> Dictionary<String, Any> {
        return ["username" : userTagged.username, "pos_x" : position[0], "pos_y" : position[1]]
    }
}
