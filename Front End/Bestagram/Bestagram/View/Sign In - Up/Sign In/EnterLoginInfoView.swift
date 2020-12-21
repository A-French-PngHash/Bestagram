//
//  EnterLoginInfoView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/12/2020.
//

import SwiftUI

struct EnterLoginInfoView: View {
    @Environment(\.presentationMode) var presentationMode

    /// Text entered bu user in the username/email field.
    @State var nameEntered : String = ""
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

    var body: some View {
        HStack {
            Spacer()
                .frame(width: 15)
            VStack(spacing: 20) {
                Spacer()
                Text("Bestagram")
                    .font(Billabong(size: 55).font)

                CustomTextField(displayCross: true, placeholder: "Username or email", input: $nameEntered, error: $textFieldErrorStyle) { (value) in
                    checkIfButtonShouldBeDisabled()
                }
                CustomTextField(displayCross: true, secureEntry: true, placeholder: "Password", distanceEdge: 0, input: $passwordEntered, error: $textFieldErrorStyle) { (value) in
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
                    textFieldErrorStyle = false
                    buttonStyle = .loading
                    let queue = DispatchQueue(label: "connect-user")
                    queue.async {
                        self.user = User(username: self.nameEntered, password: self.passwordEntered, loadingFinished: { (success, error) in
                            userFinishedLoading(success: success, error: error)
                        })
                    }
                }
                Group {
                    Spacer()
                    Divider()
                    HStack {
                        Text("Don't have an account?")
                        NavigationLink(
                            destination: EnterPhoneOrEmailView(),
                            label: {
                                Text("Sign up")
                            })
                            .foregroundColor(.blue)
                    }
                    Spacer()
                        .frame(height: 0)
                }
            }
            Spacer()
                .frame(width: 15)
        }
        .navigationBarItems(leading: BackButton(presentationMode: presentationMode))
        .navigationBarBackButtonHidden(true)
    }

    /// Update the style of the login button.
    func checkIfButtonShouldBeDisabled() {
        if passwordEntered.count > 0 && nameEntered.count > 0 {
            self.buttonStyle = .normal
        } else {
            self.buttonStyle = .disabled
        }
    }

    func userFinishedLoading(success : Bool, error : BestagramError?) {
        loadingUser = false
        buttonStyle = .normal
        if success {

        } else {
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
        EnterLoginInfoView()
            .preferredColorScheme(.dark)
            .font(ProximaNova.body)
    }
}
