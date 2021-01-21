//
//  SearchService.swift
//  Bestagram
//
//  Created by Titouan Blossier on 21/01/2021.
//

import Foundation
import Alamofire

/// Provide functionnality for searching for users.
class SearchService {
    //MARK: - Singleton
    static let shared = SearchService()
    private init() { }

    //MARK: - Urls
    let path = Api.path

    let searchUrl = "search"

    /// Search for usernames matching the given string.
    ///
    /// - parameter searchString: sername to search for.
    /// - parameter offset: Offset to get the usernames from (start at 0). (for example if the user is scrolling through the list and reach the end then the app may need to send another request to the api to get the following users. Of curse because the previous usernames have already been fetched before the app only need the new ones, use the offset to start fetching from a certain position.)
    /// - parameter rowCount: Number of results to get. According to the api documentation, can't be bigger than a 100.
    /// - Parameters:
    ///     - callback : Closure called when the response was sent.
    ///     - success: Wether or not the request reached the server. **Does not mean that the server accepted the request** (invalid credentials can still happen for example).
    ///     - usernames: If the operation was successful then this is the list of usernames the api sent.
    ///     - error: If the operation was **not** successful this is the error message included in the response.
    ///     - code: Code of the answer. If this is nil it means that no answer came back.
    ///
    func searchUser(
        searchString: String,
        offset: Int,
        rowCount: Int,
        callback : @escaping (_ success: Bool, _ usernames: Array<String>?,_ error: String?,_ code: Int?) -> Void) {
        let parameters = ["search" : searchString]
        var method : HTTPMethod = .get

        Api.session.request(path + searchUrl, method: method, parameters: parameters).responseJSON { (response) in
        }

    }
}
