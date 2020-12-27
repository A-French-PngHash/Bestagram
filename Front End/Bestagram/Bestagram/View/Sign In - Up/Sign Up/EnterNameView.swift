//
//  EnterNameView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 24/12/2020.
//

import SwiftUI

struct EnterNameView: View {
    @Environment(\.presentationMode) var presentationMode
    @Environment(\.colorScheme) var colorScheme

    /// Email entered by the user on previous views.
    var email : String

    @State var name : String = ""
    @State var textFieldErrorStyle : Bool = false
    @State var nextButtonStyle : Style = .disabled
    @State var goToNextView : Bool = false

    var body: some View {
        InterfacePositioningView(alreadyHaveAnAccount : true) {
            VStack(spacing: 20) {
                Text("Add your name")
                    .font(ProximaNova(size: 30, bold: false).font)
                Text("Add your name so that friends can find you.")
                    .multilineTextAlignment(.center)
                    .foregroundColor(.gray)

                CustomTextField(placeholder: "Full name", contentType: .name ,input: $name, error: $textFieldErrorStyle) { (value) in
                    if value.count > 0 && value.count < 40{
                        nextButtonStyle = .normal
                    } else {
                        nextButtonStyle = .disabled
                    }
                }

                BigBlueButton(text: "Next", style: $nextButtonStyle) {
                    goToNextView = true
                }
                NavigationLink(
                    destination: CreatePasswordView(email: email, name: name),
                    isActive: $goToNextView,
                    label: {
                        EmptyView()
                    })
                Spacer()
            }
        }
        .navigationBarHidden(true)
    }
}

struct EnterNameView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            EnterNameView(email: "email@gmail.com")
                .preferredColorScheme(.dark)
                .font(ProximaNova.body)
        }
    }
}
