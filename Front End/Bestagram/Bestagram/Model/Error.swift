//
//  Error.swift
//  Bestagram
//
//  Created by Titouan Blossier on 19/12/2020.
//

import Foundation

protocol BestagramError : Error {
    var description : String { get }
}

struct UnknownError : BestagramError {
    var documentation : String?

    /// Init
    ///
    /// - parameter documentation: Documentation that may be provided with the error.
    init(documentation: String?) {
        self.documentation = documentation
    }

    var description: String {
        get {
            "An unknown error happenned - \(documentation)"
        }
    }
}

struct InvalidCredentials : BestagramError {
    var description: String = "Sorry you can't be logged in as your username or password may be incorrect."
}

/// Error in case the API raises a missing information error. This should not happen because of the user, if it happen it is the result of a bug.
struct MissingInformations : BestagramError {
    var description: String = "We had problems providing all the informations to the server. Please contact a developper of the app."
}

struct UsernameAlreadyTaken : BestagramError {
    var description: String = "Sorry this username is already taken... Try a different one."
}
