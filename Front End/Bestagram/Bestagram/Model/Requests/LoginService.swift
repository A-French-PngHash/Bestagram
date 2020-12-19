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
    /// - parameter callback: Function called when the Api sent back the response. The Bool argument is wether the request succeeded or not. If it succeeded then the String is the token. In case of a failure, the optional Int is the error code.
    func fetchToken(username: String, password : String, callback : @escaping (Bool, String?, Int?) -> Void) {
        let parameters = ["username": username, "hash": password]
        Api.session.request(path + loginUrl, method: .get, parameters: parameters, encoding: JSONEncoding.default).responseJSON { (response) in
            debugPrint(response)
            guard response.error == nil && response.response?.statusCode == 200 else {
                // Error happened in the request.
                callback(false, response.error.debugDescription, response.response?.statusCode)
                return
            }
            switch response.result{
            case .failure(_):
                // Error happened in the request.
                callback(false, nil, response.response?.statusCode)
                return
            case .success(let data):
                // Request is succesful.
                guard let json = data as? Dictionary<String, String>,
                      let token = json["token"] else {
                    // Error while parsing json.
                    callback(false, nil, response.response?.statusCode)
                    return
                }
                print(token)
                callback(true, token, nil)
            }


        }
    }
}
