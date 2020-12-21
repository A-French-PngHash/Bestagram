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

    // Contain the form that is displayed to the user. The body variable really contain adjustments to make the form look good in the app.
    var form : some View {
        VStack(spacing: 20){
            Text("Enter phone number or email address")
            Picker(selection: self.$pickerSelection, label: Text("test"), content: {
                Text("Phone").tag(1)
                Text("Email").tag(2)
            })
            .pickerStyle(SegmentedPickerStyle())

            if pickerSelection == 1 {
                // Selection is phone.
                CustomTextField(
                    displayCross: true,
                    placeholder: "Email address",
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
                    input: $emailEntered, error: $textFieldErrorStyle) { (value) in
                    // Set the button style to disable or not.
                    if !Checks.isEmailValid(email: value) {
                        buttonStyle = .disabled
                    }
                }
            }
            BigBlueButton(text: "Next", style: $buttonStyle) {
                print(emailEntered)
            }
        }
    }

    var body: some View {
        VStack {
            HStack {
                Spacer()
                    .frame(width: 10)
                BackButton(presentationMode: presentationMode)
                Spacer()
            }
            HStack {
                Spacer()
                    .frame(width: 40)
                VStack{
                    form
                    Spacer()
                }
                Spacer()
                    .frame(width: 40)
            }

            Divider()
            Spacer()
                .frame(height: 20)
            HStack {
                Text("Already have an account?")
                    .font(ProximaNova.bodyBold)
                NavigationLink(
                    destination: EnterLoginInfoView(),
                    label: {
                        Text("Sign In")
                    })
                    .foregroundColor(.blue)
            }
            Spacer()
                .frame(height: 20)
        }
        .navigationBarHidden(true)
    }
}

struct EnterPhoneOrEmailView_Previews: PreviewProvider {
    static var previews: some View {
        EnterPhoneOrEmailView()
            .font(ProximaNova.body)
            .preferredColorScheme(.dark)
    }
}
