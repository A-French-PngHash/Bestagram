//
//  BigBlueButton.swift
//  Bestagram
//
//  Created by Titouan Blossier on 09/12/2020.
//

import SwiftUI

struct BigBlueButton: View {
    /// Big blue button used in different part of the app especially for login and creating an account.

    /// Text to display on the button.
    var text: String
    @Binding var disabled: Bool
    /// Action to do when button is pressed.
    var onPress : () -> Void

    var body: some View {
        Button(action: {
            onPress()
        }, label: {
            Text(self.text)
                .font(ProximaNova.bodyBold)
        })
        .padding()
        .frame(height: 35)
        .frame(maxWidth: .infinity)
        .background(Color.blue)
        .foregroundColor(.white)
        .cornerRadius(4)
        .opacity(disabled ? 0.6 : 1)
    }
}

struct BigBlueButton_Previews: PreviewProvider {
    @State static var disabled: Bool = true
    static var previews: some View {
        BigBlueButton(text: "Test", disabled: $disabled) {
            print("button clicked successfully")
        }
    }
}
