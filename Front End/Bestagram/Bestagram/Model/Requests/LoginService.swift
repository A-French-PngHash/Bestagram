//
//  LoginService.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/12/2020.
//

import Foundation
import Alamofire

/// Manage requests related to login (sign up, sign in...)
class LoginService {
    //MARK: - Singleton
    static let shared = LoginService()
    private init() { }

    //MARK: - Urls
    let path = Api.path

    let loginUrl = "login"

    //MARK: - Functions
    /// Fetch the token using the Bestagram API.
    ///
    /// - parameter username: Username to use.
    /// - parameter password: **Encrypted** password. Encrypted as indicated in the API Documentation.
    /// - parameter callback: Function called when the Api sent back the response. The Bool argument is wether the request succeeded or not. If it succeeded then the String is the token otherwise it is the error message sent back. In case of a failure, the optional Int is
    func fetchToken(username: String, password : String, callback : @escaping (Bool, String, Int?) -> Void) {
        Alamofire.AF.request(path + loginUrl, method: .get).response { (data) in
            DispatchQueue.main.async {
                //TODO: - Because of the API which uses self signed certificates, this section poses problems.
                print(data)
            }
        }
    }
}
