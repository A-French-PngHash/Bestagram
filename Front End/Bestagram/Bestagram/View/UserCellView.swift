//
//  UserCellView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/03/2021.
//

import SwiftUI

struct UserCellView: View {
    var user : User
    var body: some View {
        HStack {
            Group {
                if let profilePicture = user.profilePicture {
                    Image(uiImage: profilePicture)
                } else {
                    Circle()
                        .foregroundColor(.gray)
                        .frame(width:50, height: 50)
                }
                VStack {
                    HStack {
                        Text(user.username!)
                            .font(ProximaNova.bodyBold)
                        Spacer()
                    }
                    HStack {
                        Text(user.name!)
                        Spacer()
                    }
                }
            }
        }
        .padding()
    }
}

struct UserCellView_Previews: PreviewProvider {
    static var previews: some View {
        UserCellView(user: User(id: 3, username: "bill gates", name: "bill.gates"))
    }
}
