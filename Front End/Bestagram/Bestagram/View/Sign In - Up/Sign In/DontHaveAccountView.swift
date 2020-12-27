//
//  DontHaveAccountView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 26/12/2020.
//

import SwiftUI

struct DontHaveAccountView: View {
    var body: some View {
        VStack {
            Divider()
            HStack {
                Text("Don't have an account?")
                    .foregroundColor(.gray)
                NavigationLink(
                    destination: EnterPhoneOrEmailView(),
                    label: {
                        Text("Sign up")
                    })
                    .foregroundColor(.blue)
            }
        }
    }
}

struct DontHaveAccountView_Previews: PreviewProvider {
    static var previews: some View {
        DontHaveAccountView()
    }
}
