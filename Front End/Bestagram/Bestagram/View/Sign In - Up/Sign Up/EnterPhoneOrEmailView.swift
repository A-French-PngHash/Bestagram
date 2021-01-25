//
//  EnterPhoneOrEmailView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 09/12/2020.
//

import SwiftUI

struct EnterPhoneOrEmailView: View {

    @Environment(\.presentationMode) var presentationMode
    @Environment(\.colorScheme) var colorScheme

    @State var pickerSelection: Int = 2
    @State var emailEntered: String = ""
    /// Style the next button should have.
    @State var buttonStyle: Style = .disabled
    /// Apply error style to text field.
    @State var textFieldErrorStyle: Bool = false
    /// Error description.
    @State var errorDescription : String = ""
    @State var goToNextView = false

    var body: some View {
        InterfacePositioningView(alreadyHaveAnAccount : true) {
            VStack(spacing: 20){
                Text("Enter phone number or email address")
                    .multilineTextAlignment(.center)
                    .foregroundColor(.gray)
                Picker(selection: self.$pickerSelection, label: Text("test"), content: {
                    Text("Phone").tag(1)
                    Text("Email").tag(2)
                })
                .pickerStyle(SegmentedPickerStyle())

                if pickerSelection == 1 {
                    // Selection is phone.
                    CustomTextField(
                        displayCross: true,
                        placeholder: "Enter Phone",
                        input: $emailEntered, error: $textFieldErrorStyle) { (value) in
                        // Set the button style to disable or not.
                        if !Checks.isEmailValid(email: value) {
                            buttonStyle = .disabled
                        }
                    }
                } else if pickerSelection == 2 {
                    // Selection is email.
                    CustomTextField(
                        displayCross: true,
                        placeholder: "Email address",
                        contentType: .emailAddress,
                        input: $emailEntered, error: $textFieldErrorStyle) { (value) in
                        // Set the button style to disable or not.
                        if Checks.isEmailValid(email: value) {
                            buttonStyle = .normal
                        } else {
                            buttonStyle = .disabled
                        }
                    }
                }
                if textFieldErrorStyle {
                    Text(errorDescription)
                        .foregroundColor(.red)
                }
                BigBlueButton(text: "Next", style: $buttonStyle) {
                    buttonStyle = .loading
                    LoginService.shared.checkIfEmailTaken(email: emailEntered) { (success, taken) in
                        buttonStyle = .normal
                        textFieldErrorStyle = true
                        guard let taken = taken, success else {
                            self.errorDescription = "Connection error, please check your connection and try again later."
                            return
                        }
                        if taken {
                            self.errorDescription = "This adress email already belongs to an account."
                        } else {
                            textFieldErrorStyle = false
                            goToNextView = true
                        }
                    }
                }

                NavigationLink(
                    destination: EnterUsernameView(email: emailEntered),
                    isActive: $goToNextView,
                    label: {
                        Text("")
                    })
            }
        }
        .navigationBarHidden(true)
    }
}

struct EnterPhoneOrEmailView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            EnterPhoneOrEmailView()
                .font(ProximaNova.body)
                .preferredColorScheme(.dark)
        }
    }
}
