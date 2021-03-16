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
    /// Style the button should take.
    var style: Style
    /// Action to do when button is pressed.
    var onPress : () -> Void

    var body: some View {
        Button(action: {
            onPress()
        }, label: {
            Group {
                if style == .loading {
                    ProgressView()
                } else {
                    Text(self.text)
                        .font(ProximaNova.body)
                }
            }
            .padding()
            .frame(height: 37)
            .frame(maxWidth: .infinity)
        })
        .background(Color.blue)
        .foregroundColor(.white)
        .cornerRadius(4)
        .opacity(style == .disabled || style == .loading ? 0.6 : 1)
        .disabled(style == .disabled || style == .loading)
    }
}

enum Style {
    case disabled, loading, normal
}

struct BigBlueButton_Previews: PreviewProvider {
    static var previews: some View {
        BigBlueButton(text: "Test", style: .normal) {
            print("button clicked successfully")
        }
    }
}
