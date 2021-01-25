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
            if let doc = documentation {
                return "An unknown error happenned - \(String(describing: doc))"
            } else {
                return "An unknown error happenned"
            }
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
    var description: String = "This username is already taken... Try a different one."
}

struct EmailAlreadyTaken : BestagramError {
    var description: String = "This email is already taken..."
}

struct InvalidEmailAdress : BestagramError {
    var description: String = "The email adress provided is invalid."
}

struct InvalidUsername : BestagramError {
    var description: String = "This username is not valid."
}

struct InvalidEmail : BestagramError {
    var description: String = "This email is not valid."
}

struct InvalidName : BestagramError {
    var description: String = "Your name is not valid... Try removing special characters you may have put inside."
}

struct ConnectionError : BestagramError {
    var description: String = "Connection error, please check your connection and try again later."
}
