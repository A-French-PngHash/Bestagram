//
//  EnterLoginInfoView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/12/2020.
//

import SwiftUI

struct EnterLoginInfoView: View {
    @Environment(\.presentationMode) var presentationMode

    /// Text entered bu user in the username field.
    @State var usernameEntered : String = ""
    /// Text entered by user in the password field.
    @State var passwordEntered : String = ""
    /// Style the next button should have.
    @State var buttonStyle: Style = .disabled
    /// User object when the user has entered its info and the data has been succesfully fetched.
    @State var user: User? = nil
    /// Wether the user is being loaded or not.
    @State var loadingUser : Bool = false
    /// Apply error style to text field.
    @State var textFieldErrorStyle: Bool = false
    /// If the user login failed, this is the message that will be displayed to inform the user on what failed.
    @State var errorDescription: String = ""
    /// Wether or not the loading of the user token with the provided
    /// information was succesful or not.
    @State var loadingSucceeded: Bool = false

    var body: some View {
        InterfacePositioningView(dontHaveAnAccount: true) {
            VStack(spacing: 20) {
                Spacer()
                Text("Bestagram")
                    .font(Billabong(size: 55).font)

                CustomTextField(
                    displayCross: true,
                    placeholder: "Username",
                    contentType: .username,
                    input: $usernameEntered,
                    error: $textFieldErrorStyle) { (value) in
                    checkIfButtonShouldBeDisabled()
                }
                CustomTextField(
                    displayCross: true,
                    secureEntry: true,
                    placeholder: "Password",
                    contentType: .password,
                    input: $passwordEntered,
                    error: $textFieldErrorStyle) { (value) in
                    checkIfButtonShouldBeDisabled()
                }
                if textFieldErrorStyle {
                    // Error happenned, displaying error message to the user.
                    Text(errorDescription)
                        .foregroundColor(.red)
                }
                HStack {
                    Spacer()
                    Button(action: {
                        //TODO: Implement password recuperation.
                    }, label: {
                        Text("Forgotten password ?")
                    })
                }
                BigBlueButton(text: "Log In", style: $buttonStyle) {
                    loadingUser = true
                    loadingSucceeded = false
                    textFieldErrorStyle = false
                    buttonStyle = .loading
                    let queue = DispatchQueue(label: "connect-user")
                    queue.async {
                        // Loging will automatically start the hashing process and the fetch of the token.
                        self.user = User(authenticationFinished: { (success, token, error) in
                            userFinishedLoading(success: success, error: error)
                        })
                    }
                }

                NavigationLink(
                    destination: Text("main page"),
                    isActive: $loadingSucceeded,
                    label: {
                        EmptyView()
                    })
                Spacer()
            }
        }
        .navigationBarHidden(true)
    }

    /// Update the style of the login button.
    func checkIfButtonShouldBeDisabled() {
        if passwordEntered.count > 0 && usernameEntered.count > 0 {
            self.buttonStyle = .normal
        } else {
            self.buttonStyle = .disabled
        }
    }

    func userFinishedLoading(success : Bool, error : BestagramError?) {
        loadingUser = false
        buttonStyle = .normal
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

struct EnterLoginInfoView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            EnterLoginInfoView()
                .preferredColorScheme(.dark)
                .font(ProximaNova.body)
        }
    }
}
