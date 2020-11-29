//
//  Description.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import Foundation

class Description {
    /// Store data about a description entered by a user. Can be profile description, post description...

    /// The full description is all the text entered by the user when they added it.
    let fullDescription: String
    /// The reduced description is what is shown to the user when they scroll through.
    /// They can decide to click on it to show the full description.
    var reducedDescription: String! = nil
    // swiftlint:disable:previous implicitly_unwrapped_optional

    init(text: String) {
        self.fullDescription = text
        self.reducedDescription = getReducedDescriptionFrom(description: text)
    }

    /// Calculate and return the reduced description using certain rules.
    ///
    /// The reduced description can't cut a word in half (except if its a really big word)
    /// and has a minimum of characters.
    private func getReducedDescriptionFrom(description: String) -> String {
        var index = Post.minimumCharacterReducedDescription
        while
            description.count > index &&
            description[index] != " " &&
            Post.minimumCharacterReducedDescription - index <= 10 {
            index += 1
        }

        // The reduced description is the same as the full.
        if index == description.count {
            return description
        } else {
            // The reduced description is smaller than the full.
            return String(description.prefix(index))
            // NOTE : When the reduced description is shown to the user, there should be a "... more" at then end.
            // The programm doesn't add it here as it needs to be in a different color
            // and it can't do that if it's all in the same string.
        }
    }
}
