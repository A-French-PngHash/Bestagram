//
//  Caption.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import Foundation

class Caption {
    /// Store data about a caption entered by a user. Can be profile caption, post caption...

    /// The full caption is all the text entered by the user when they added it.
    let fullCaption: String
    /// The reduced caption is what is shown to the user when they scroll through.
    /// They can decide to click on it to show the full caption.
    var reducedCaption: String! = nil
    // swiftlint:disable:previous implicitly_unwrapped_optional

    init(text: String) {
        self.fullCaption = text
        self.reducedCaption = getReducedCaptionFrom(caption: text)
    }

    /// Calculate and return the reduced caption using certain rules.
    ///
    /// The reduced caption can't cut a word in half (except if its a really big word)
    /// and has a minimum of characters.
    private func getReducedCaptionFrom(caption: String) -> String {
        var index = Post.minimumCharacterReducedCaption
        while
            caption.count > index &&
            caption[index] != " " &&
            Post.minimumCharacterReducedCaption - index <= 10 {
            index += 1
        }

        // The reduced caption is the same as the full.
        if index == caption.count {
            return caption
        } else {
            // The reduced caption is smaller than the full.
            return String(caption.prefix(index))
            // NOTE : When the reduced caption is shown to the user, there should be a "... more" at then end.
            // The programm doesn't add it here as it needs to be in a different color
            // and it can't do that if it's all in the same string.
        }
    }
}
