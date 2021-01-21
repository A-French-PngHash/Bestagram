//
//  SignInOrUpChoiceView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 09/12/2020.
//

import SwiftUI

struct SignInOrUpChoiceView: View {
    /// Class giving the choice to the user between login or creating an account.

    @Environment(\.presentationMode) var presentationMode

    var body: some View {
        NavigationView {
            VStack {
                Text("Bestagram")
                    .font(Billabong(size: 55).font)
                Spacer()
                    .frame(height: 40)

                 HStack {
                     Spacer()
                         .frame(width: 25)
                     NavigationLink(destination: EnterPhoneOrEmailView()) {
                         Text("Create New Account")
                             .font(ProximaNova.bodyBold)
                     }
                     .padding(0.0)
                     .frame(height: 30)
                     .frame(maxWidth: .infinity)
                     .background(Color.blue)
                     .foregroundColor(.white)
                     .cornerRadius(5)

                     Spacer()
                         .frame(width: 25)
                 }

                Spacer()
                    .frame(height: 15)
                NavigationLink(destination: EnterLoginInfoView()) {
                    Text("Log In")
                        .font(ProximaNova.bodyBold)
                }
            }
            .navigationBarHidden(true)
            .navigationBarBackButtonHidden(false)
        }
    }
}

struct SignInOrUpChoiceView_Previews: PreviewProvider {
    static var previews: some View {
        SignInOrUpChoiceView()
            .preferredColorScheme(.dark)
            .font(ProximaNova.body)
    }
}
