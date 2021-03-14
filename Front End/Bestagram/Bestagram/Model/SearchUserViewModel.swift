//
//  SearchUserViewModel.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/03/2021.
//

import Foundation

class SearchUserViewModel : ObservableObject{
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
}
