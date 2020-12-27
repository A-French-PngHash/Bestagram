//
//  EnterConfirmationCodeView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 12/12/2020.
//

import SwiftUI

/// THIS VIEW IS NOT IMPLEMENTED FOR THE MOMENT AS THE API IS CURRENTLY NOT SENDING ANY EMAIL.

/// Display a text field to the user asking him to validate the confirmation code that was sent to his email.
struct EnterConfirmationCodeView: View {

    /// Email entered by the user.
    var email: String

    /// Style the next button should have.
    @State var buttonStyle: Style = .disabled
    /// Code entered by user in the text field.
    @State var code: String = ""
    /// Apply error style to text field.
    @State var textFieldErrorStyle: Bool = false

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
                    distanceEdge: 0, contentType: .name, input: $code, error : $textFieldErrorStyle) { (value) in
                    if value.count != codeLength {
                        buttonStyle = .disabled
                    }
                }
                BigBlueButton(text: "Next", style: $buttonStyle) {
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
