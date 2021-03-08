//
//  CreatePasswordView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 25/12/2020.
//

import SwiftUI

struct CreatePasswordView: View {

    var email : String
    var name : String
    var username : String

    @State var user : User?
    
    @State var textFieldErrorStyle = false
    @State var password = ""
    @State var buttonStyle : Style = .disabled
    @State var savePasswordTicked = true
    @State var goNextView = false
    /// Error to show if there was an error during registration.
    @State var displayedError = ""


    var body: some View {
        InterfacePositioningView(alreadyHaveAnAccount : true) {
            VStack(spacing: 20){
                Text("Create a password")
                    .font(ProximaNova(size: 30, bold: false).font)
                Text("We can remember the password, so you won't need to enter it on your Icloud devices")
                    .multilineTextAlignment(.center)
                    .foregroundColor(.gray)
                CustomTextField(
                    secureEntry: true,
                    placeholder: "Password",
                    contentType: .password,
                    input: $password,
                    error: $textFieldErrorStyle) { (value) in
                    if value.count > 7 && value.count < 40 {
                        buttonStyle = .normal
                    } else {
                        buttonStyle = .disabled
                    }
                }
                HStack {
                    Image(systemName: savePasswordTicked ? "checkmark.square.fill" : "square")
                        .onTapGesture {
                            savePasswordTicked = !savePasswordTicked
                        }
                        .foregroundColor(.blue)
                    Text("Save password")
                        .foregroundColor(.gray)
                    Spacer()
                    //TODO: - Implement password saving.
                }
                // We can now register the creation of the account.
                BigBlueButton(text: "Next", style: $buttonStyle) {
                    let queue = DispatchQueue(label: "signup")
                    buttonStyle = .loading
                    queue.async {
                        // We create the user here. If the operation is successful, the credentials are saved.
                        User.create(username: username.lowercased(), password: password, email: email, name: name, callback: { (success, error) in
                                if success {
                                    goNextView = true
                                } else {
                                    if let err = error?.description {
                                        displayedError = err
                                    }
                                }
                                buttonStyle = .normal
                        })
                    }
                }
                if displayedError != "" {
                    Text(displayedError)
                        .foregroundColor(.red)
                }
                if (user != nil) {
                    NavigationLink(
                        destination: WelcomeToBestagramView(user: user!),
                        isActive: $goNextView,
                        label: {
                            EmptyView()
                    })
                }
            }
        }
        .navigationBarHidden(true)
    }
}

struct CreatePasswordView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            CreatePasswordView(email: "email@bestagram", name: "name", username: "username")
                .font(ProximaNova.body)
                .preferredColorScheme(.dark)
        }
    }
}
