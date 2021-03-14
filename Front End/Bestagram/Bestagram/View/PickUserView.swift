//
//  PickUsernameView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 21/01/2021.
//

import SwiftUI

/// Display a search bar, a keyboard and a list of username. Make call to the API.
struct PickUserView: View {

    /// Closure called when the user picked a username. Send the username as the first argument.
    var onUserPicked : (User) -> Void
    /// Closure called when the user click the cancel button.
    var onCancelButtonPressed : () -> Void
    var user : User

    /// List of users sent back by the API.
    @Published var users : Array<User> = []
    @State var searchInput : String = ""
    /// Wether or not a list of username is currently been fecthed from the api.
    @State var searchInProgress : Bool = true

    /// When there is an error fetching result a view is displayed (ErrorView). This variable indicates wether it should be shown.
    @State var displayErrorView : Bool = false
    /// Error message to include in the error view if it is to be shown.
    @State var errorMessage : String = ""
    /// Delay before the error view is hidden again.
    let errorViewDisapearanceDelay : Int = 3


    var body: some View {
        VStack {
            HStack {
                SearchBar(placeholder: "Search for a person", height: 30, input: $searchInput, onEdit: { (input) in
                    search()
                })
                .padding(5)

                Button(action: {
                    onCancelButtonPressed()
                }, label: {
                    Text("Cancel")
                        .font(ProximaNova.init(size: 20, bold: false).font)
                })
                .padding(5)
            }
            Spacer()
                .frame(height: 5)
            if searchInProgress {
                HStack {
                    ProgressView()
                    Spacer()
                        .frame(width: 20)
                    Text("Searching for \"\(self.searchInput)\"")
                }
            } else {
                if users.count == 0 {
                    Text("No users found")
                    Divider()
                }

                ForEach(users, id: \.id) { user in
                    HStack {
                        UserCellView(user: user)
                        Spacer()
                    }

                }
            }
            Spacer()
            if displayErrorView {
                HStack {
                    Spacer()
                    ErrorView(errorText: errorMessage)
                    Spacer()
                }
                .transition(.move(edge: .bottom))
            }
            Spacer()
                .frame(height: 15)
        }
        .navigationBarHidden(true)
        .onAppear(perform: {
            search()
        })
    }

    /// Execute a search using this view's local data and load the result into the usernames dictionary.
    func search() {
        user.getToken { (success, token, error) in
            if let token = token, success {
                print(token)
                SearchService.shared.searchUser(searchString: searchInput, offset: 0, rowCount: 5, token: token) { (success, users, error) in
                    if success {
                        self.users = users!
                    } else {
                        manageError(error: error)
                    }
                    searchInProgress = false
                }
            } else {
                manageError(error: error)
            }
        }
    }

    /// Set variables to the right state for the error message to be displayed to the user.
    func manageError(error: BestagramError?) {
        self.users = []
        if error == BestagramError.ConnectionError {
            self.errorMessage = "Couldn't load search results"
        } else {
            self.errorMessage = "An unexpected error happened"
        }
        withAnimation {
            self.displayErrorView.toggle()
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + Double(self.errorViewDisapearanceDelay), execute: {
            withAnimation {
                self.displayErrorView.toggle()
            }
        })
    }
}

// Note that if you want to run search on your computer with xcode preview you will need to change this line to reference the credentials of an account already existing in your local database.
let testUser = User(username: "titouan_hello", password: "password") { (_, _, _) in }

struct PickUserView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            PickUserView(
                onUserPicked: {(_) in },
                onCancelButtonPressed: { },
                user: testUser
            )
        }
        .colorScheme(.dark)
        .preferredColorScheme(.dark)
        .font(ProximaNova.body)
    }
}
