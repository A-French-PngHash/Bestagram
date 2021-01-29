//
//  SearchPeopleView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 01/01/2021.
//

import SwiftUI

struct SearchPeopleView: View {
    @State var error: BestagramError = BestagramError.UnknownError
    var body: some View {
        VStack {
            Text(error.description)
            Button(action: {
                /*
                let user = User.create(username: "titouana", password: "password", email: "titouan@bestagram.com", name: "titouane blossier", save: true) { (success, error) in
                    if let err = error {
                        self.error = err
                    }
                }
                */
                let user = User(credentialsSaved: true, username: nil, password: nil, saveCredentials: nil)
                user.getToken { (success, token, error) in
                    if let token = token, success {
                        SearchService.shared.searchUser(searchString: "africa", offset: 0, rowCount: 5, token: token) { (success, usernames, error) in
                            print(usernames)

                        }
                    }
                }

            }, label: {
                Text("button")
            })

        }
    }
}

struct SearchPeopleView_Previews: PreviewProvider {
    static var previews: some View {
        SearchPeopleView()
    }
}
