//
//  Error.swift
//  Bestagram
//
//  Created by Titouan Blossier on 19/12/2020.
//

import Foundation

public enum BestagramError {
    case UnknownError, InvalidCredentials, MissingInformations, UsernameAlreadyTaken, EmailAlreadyTaken, InvalidEmailAdress, InvalidUsername, InvalidEmail, InvalidName, InvalidJson, ConnectionError, NonAuthenticatedUser

    var description : String {
        switch self{
        case .UnknownError:
            return "An unknown error happenned."
        case .InvalidCredentials:
            return "Sorry you can't be logged in as your username or password may be incorrect."
        case .MissingInformations:
            // Error in case the API raises a missing information error.
            // This should not happen because of the user, if it happen it is the result of a bug.
            return "We had problems providing all the informations to the server. Please contact a developper of the app."
        case .UsernameAlreadyTaken:
            return  "This username is already taken... Try a different one."
        case .EmailAlreadyTaken:
            return "This email is already taken..."
        case .InvalidEmailAdress:
            return "The email adress provided is invalid."
        case .InvalidUsername:
            return "This username is not valid."
        case .InvalidEmail:
            return "This email is not valid."
        case .InvalidName:
            return "Your name is not valid... Try removing special characters you may have put inside."
        case .InvalidJson:
            return "The response sent back from the server is invalid."
        case .ConnectionError:
            return "Connection error, please check your connection and try again later."
        case .NonAuthenticatedUser: // Should not happen, this is only in case of the developper messing up with the innits of the user class.
            return "This user is not authenticated thus it's token cannot be retrieved."
        }
    }
}
