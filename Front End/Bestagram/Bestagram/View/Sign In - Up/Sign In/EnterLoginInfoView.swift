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
    /// State to set the log in button to. Disable or not.
    @State var buttonDisabled : Bool = true

    var body: some View {
        HStack {
            Spacer()
                .frame(width: 15)
            VStack(spacing: 20) {
                Spacer()
                Text("Bestagram")
                    .font(Billabong(size: 55).font)

                CustomTextField(displayCross: true, placeholder: "Username or email", input: $nameEntered) { (value) in
                    checkIfButtonShouldBeDisabled()
                }
                CustomTextField(displayCross: true, secureEntry: true, placeholder: "Password", distanceEdge: 0, input: $passwordEntered) { (value) in
                    checkIfButtonShouldBeDisabled()
                }
                HStack {
                    Spacer()
                    Button(action: {
                        //TODO: Implement password recuperation.
                    }, label: {
                        Text("Forgotten password ?")
                    })
                }
                BigBlueButton(text: "Log In", disabled: $buttonDisabled) {
                    //TODO: Do something when log in button pressed
                }
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
            Spacer()
                .frame(width: 15)
        }
        .navigationBarItems(leading: BackButton(presentationMode: presentationMode))
        .navigationBarBackButtonHidden(true)
    }

    /// Update the buttonDisabled variable
    func checkIfButtonShouldBeDisabled() {
        self.buttonDisabled = !(passwordEntered.count > 0 && nameEntered.count > 0)
    }
}

struct EnterLoginInfoView_Previews: PreviewProvider {
    static var previews: some View {
        EnterLoginInfoView()
            .preferredColorScheme(.dark)
            .font(ProximaNova.body)
    }
}
