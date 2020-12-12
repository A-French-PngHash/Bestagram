//
//  EnterConfirmationCodeView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 12/12/2020.
//

import SwiftUI

/// Display a text field to the user asking him to validate the confirmation code that was sent to his email.
struct EnterConfirmationCodeView: View {

    /// Email entered by the user.
    var email: String

    /// Disable or not the next button.
    @State var buttonDisabled: Bool = true
    /// Code entered by user in the text field.
    @State var code: String = ""

    /// The length of the code sent to the user.
    let codeLength = 6

    var body: some View {
        HStack {
            Spacer()
                .frame(width: 35)
            VStack {
                Text("Enter confirmation code")
                    .font(ProximaNova(size: 27, bold: false).font)
                Spacer()
                    .frame(height: 10)
                Text("Enter the confirmation we sent to \(email).")
                Button(action: {
                    // Send verification code here
                }, label: {
                    Text("Resend code")
                })
                CustomTextField(
                    displayCross: true,
                    placeholder: "Confirmation Code",
                    distanceEdge: 0, input: $code) { (value) in
                    buttonDisabled = value.count != codeLength
                }
                BigBlueButton(text: "Next", disabled: $buttonDisabled) {
                    // Go to next view
                }
                Spacer()
            }
            .multilineTextAlignment(.center)
            Spacer()
                .frame(width: 35)
        }
    }
}

struct EnterConfirmationCodeView_Previews: PreviewProvider {
    static var previews: some View {
        EnterConfirmationCodeView(email: "test.test@bestagram.com")
            .font(ProximaNova.body)
            .preferredColorScheme(.dark)
    }
}
