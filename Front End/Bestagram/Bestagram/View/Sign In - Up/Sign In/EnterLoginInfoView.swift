//
//  EnterLoginInfoView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/12/2020.
//

import SwiftUI

struct EnterLoginInfoView<Model: EnterLoginInfoViewModel>: View {
    @Environment(\.presentationMode) var presentationMode

    @EnvironmentObject var model: Model

    var body: some View {
        VStack(spacing: 20) {
            Spacer()
            Text("Bestagram")
                .font(Billabong(size: 55).font)

            CustomTextField(
                displayCross: true,
                placeholder: "Username",
                contentType: .username,
                input: $model.username,
                error: model.textFieldErrorStyle)

            CustomTextField(
                displayCross: true,
                secureEntry: true,
                placeholder: "Password",
                contentType: .password,
                input: $model.password,
                error: model.textFieldErrorStyle)

            if model.textFieldErrorStyle {
                // Error happenned, displaying error message to the user.
                Text(model.errorDescription)
                    .foregroundColor(.red)
            }
            HStack {
                Spacer()
                Button(action: {
                    //TODO: Implement password recovery.
                }, label: {
                    Text("Forgotten password ?")
                })
            }
            BigBlueButton(text: "Log In", style: model.buttonStyle) {
                model.loginButtonPressed()
            }

            NavigationLink(
                destination: Text("main page"),
                isActive: $model.loadingSucceeded,
                label: {
                    EmptyView()
                })
            Spacer()
        }
        .navigationBarHidden(true)
        .modifier(InterfacePositioning(dontHaveAnAccount: true))
    }
}

struct EnterLoginInfoView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            EnterLoginInfoView()
                .environmentObject(EnterLoginInfoViewModel())
                .preferredColorScheme(.dark)
                .font(ProximaNova.body)
        }
    }
}
