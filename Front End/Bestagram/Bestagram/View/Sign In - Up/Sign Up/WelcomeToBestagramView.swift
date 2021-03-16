//
//  WelcomeToBestagramView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 25/12/2020.
//

import SwiftUI

struct WelcomeToBestagramView: View {

    var user : User
    
    var body: some View {
        HStack {
            Spacer()
                .frame(width: 20)
            VStack(spacing: 20) {
                Text("Welcome to Bestagram, \(user.name!)")
                    .font(ProximaNova(size: 25, bold: false).font)
                    .multilineTextAlignment(.center)
                Text("Find people to follow and start sharing photos. You can change your username at any time.")
                    .multilineTextAlignment(.center)
                    .foregroundColor(.gray)
                BigBlueButton(text: "Next", style: .normal) {
                    print("next")
                }
                Spacer()
            }
            Spacer()
                .frame(width: 20)
        }
        .navigationBarHidden(true)
    }
}

struct WelcomeToBestagramView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            WelcomeToBestagramView(user: defaultUser)
                .preferredColorScheme(.dark)
        }

    }
}
