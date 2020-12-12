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
    @State var buttonDisabled: Bool = true

    var body: some View {
        VStack {
            Text("Enter phone number or email adress")
            Spacer()
                .frame(height: 30)
            HStack {
                Spacer()
                    .frame(width: 20)
                Picker(selection: self.$pickerSelection, label: Text("test"), content: {
                    Text("Phone").tag(1)
                    Text("Email").tag(2)
                })
                .pickerStyle(SegmentedPickerStyle())
                Spacer()
                    .frame(width: 20)
            }
            Spacer()
                .frame(height: 10)
            if pickerSelection == 1 {
                // Selection is phone.
                CustomTextField(
                    displayCross: true,
                    placeholder: "Email address",
                    distanceEdge: 20,
                    input: $emailEntered) { (value) in
                    // Set the variable to disable or not the button style.
                    buttonDisabled = !Checks.isEmailValid(email: value)
                }
            } else if pickerSelection == 2 {
                // Selection is email.
                CustomTextField(
                    displayCross: true,
                    placeholder: "Email address",
                    distanceEdge: 20,
                    input: $emailEntered) { (value) in
                    // Set the variable to disable or not the button style.
                    buttonDisabled = !Checks.isEmailValid(email: value)
                }
            }
            Spacer()
                .frame(height: 10)
            BigBlueButton(
                text: "Next",
                disabled: $buttonDisabled) {
                print(emailEntered)
            }
            Spacer()
        }
        .navigationBarItems(leading: BackButton(presentationMode: presentationMode))
        .navigationBarBackButtonHidden(true)

    }
}

struct EnterPhoneOrEmailView_Previews: PreviewProvider {
    static var previews: some View {
        EnterPhoneOrEmailView()
            .font(ProximaNova.body)
            .preferredColorScheme(.dark)
    }
}
