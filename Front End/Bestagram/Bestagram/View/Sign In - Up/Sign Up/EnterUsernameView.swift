//
//  EnterUsernameView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 22/01/2021.
//

import SwiftUI

struct EnterUsernameView: View {
    var email: String

    @State var username: String = ""
    @State var textFieldShouldDisplayError: Bool = false
    @State var buttonStyle: Style = .disabled
    @State var goNextView = false

    var body: some View {
        InterfacePositioningView(showBackButton: true, alreadyHaveAnAccount: true, dontHaveAnAccount: false) {
            VStack(spacing: 20) {
                Text("Create username")
                    .font(ProximaNova(size: 30, bold: false).font)
                Text("Choose a username for your new account. You can always change it later.")
                    .multilineTextAlignment(.center)
                CustomTextField(placeholder: "Username", input: $username, error: $textFieldShouldDisplayError) { (new) in
                    if new.count < 5 || new.count > 30 {
                        buttonStyle = .disabled
                    } else {
                        buttonStyle = .normal
                    }
                    var newUsername = ""
                    for i in new {
                        if BestagramApp.allowedUsernameCharacters.contains(i.lowercased()) && newUsername.count < 31{
                            // Valid character.
                            newUsername = "\(newUsername)\(i)"
                        }
                    }
                    username = newUsername
                }
                BigBlueButton(text: "Next", style: $buttonStyle) {
                    goNextView = true
                }
                NavigationLink(
                    destination: EnterNameView(email: email, username: username),
                    isActive: $goNextView,
                    label: {
                        Text("")
                    })
            }
        }.navigationBarHidden(true)
    }
}

struct EnterUsernameView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            EnterUsernameView(email: "test")
                .preferredColorScheme(.dark)
                .font(ProximaNova.body)
        }
    }
}
