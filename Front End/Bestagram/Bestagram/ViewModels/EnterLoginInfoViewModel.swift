//
//  EnterLoginInfoViewModel.swift
//  Bestagram
//
//  Created by Titouan Blossier on 14/03/2021.
//

import Foundation

class EnterLoginInfoViewModel : ObservableObject {

    /// Text entered by user in the username field.
    @Published var username : String = ""
    /// Text entered by user in the password field.
    @Published var password : String = ""

    /// Wether the user is being loaded or not.
    @Published var loadingUser : Bool = false

    /// Wether or not the loading of the user token with the provided
    /// information was succesful or not.
    @Published var loadingSucceeded : Bool = false

    /// Style the "next" button should have.
    var buttonStyle: Style {
        if loadingUser {
            return .loading
        }
        if password.count > 0 && username.count > 0 {
            return .normal
        } else {
            return .disabled
        }
    }

    /// Apply error style to text field.
    @Published var textFieldErrorStyle: Bool = false

    /// If the user login failed, this is the message that will be displayed to inform the user on what failed.
    @Published var errorDescription: String = ""

    /// User object when the user has entered its info and the data has been succesfully fetched.
    @Published var user : User?

    func loginButtonPressed() {
        loadingUser = true
        loadingSucceeded = false
        textFieldErrorStyle = false
        let queue = DispatchQueue(label: "connect-user")
        queue.async {
            // Loging will automatically start the hashing process and the fetch of the token.
            self.user = User(username: self.username, password: self.password, authenticationFinished: { (success, token, error) in
                self.userFinishedLoading(success: success, error: error)
            })
        }
    }

    func userFinishedLoading(success : Bool, error : BestagramError?) {
        loadingUser = false
        loadingSucceeded = success
        if !success {
            self.user = nil
            textFieldErrorStyle = true
            if let err = error {
                self.errorDescription = err.description
            }
        }
    }
}
