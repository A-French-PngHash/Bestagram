//
//  AlreadyHaveAccountView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 25/12/2020.
//

import SwiftUI

struct AlreadyHaveAccountView: View {
    var body: some View {
        VStack {
            Divider()
            Spacer()
                .frame(height: 10)
            HStack {
                Text("Already have an account?")
                    .foregroundColor(Color.gray)

                NavigationLink(
                    destination: EnterLoginInfoView(),
                    label: {
                        Text("Sign In")
                    })
                    .foregroundColor(.blue)
            }
            Spacer()
                .frame(height: 10)
        }
    }
}

struct AlreadyHaveAccountView_Previews: PreviewProvider {
    static var previews: some View {
        AlreadyHaveAccountView()
    }
}
