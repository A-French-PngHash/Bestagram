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
    let checkEmailTakenUrl = "email/taken"

    //MARK: - Functions
    /// Fetch the token using the Bestagram API. Have the option of creating the user.
    ///
    /// - parameter username: Username to use.
    /// - parameter password: **Encrypted** password. Encrypted as indicated in the API Documentation.
    /// - Parameters:
    ///     - callback: Closure called when the API sent back the response.
    ///     - success : Wether the request succeeded or not.
    ///     - content: If the request succeeded then this contain the token. If the request failed then this contain the error documentation provided by the API.
    ///     - code: HTTPStatusCode describing the operation.
    ///
    func fetchToken(username: String, password : String, register : Bool, callback : @escaping (_ success: Bool, _ content: String?, _ code: Int?) -> Void) {
        let parameters = ["username": username, "hash": password]

        // The main difference between the user being logged in/registered is the method used.
        var method : HTTPMethod = .get
        if register {
            method = .put
        }

        Api.session.request(path + loginUrl, method: method, parameters: parameters).responseJSON { (response) in

            switch response.result{
            case .failure(_):
                // Error happened BEFORE the request. In this case the request never reached the server.
                callback(false, nil, response.response?.statusCode)
                return

            case .success(let data):
                // If the REGISTER was succesful then 201 is sent back but if the LOGIN was succesful then 200 is set back.
                guard response.error == nil && (response.response?.statusCode == 200 || response.response?.statusCode == 201)  else {
                    // Error happened DURING the request.
                    let error = self.parseErrorDescription(data: data)
                    callback(false, error, response.response?.statusCode)
                    return
                }

                guard let json = data as? Dictionary<String, String>,
                      let token = json["token"] else {
                    // Error while parsing json.
                    callback(false, nil, response.response?.statusCode)
                    return
                }
                callback(true, token, response.response?.statusCode)
            }
        }
    }

    /// Check if a given email is already registered with a user.
    ///
    /// - parameter email: Email to check
    /// - Parameters:
    ///     - callback: Closure called when the API answered.
    ///     - success: Success of the request.
    ///     - emailTaken: Result of the request, wether the email is taken or not.
    func checkIfEmailTaken(email: String, callback : @escaping (_ success: Bool, _ emailTaken: Bool?) -> Void) {
        let parameters = ["email" : email]
        Api.session.request(path + checkEmailTakenUrl, method: .get, parameters: parameters).responseJSON { (response) in
            switch response.result {
            case .failure(_):
                callback(false, nil)
            case .success(let data):
                guard response.error == nil,
                      let json = data as? Dictionary<String, Bool>,
                      let taken = json["taken"] else {
                    callback(false, nil)
                    return
                }
                callback(true, taken)
            }
        }
    }

    /// According to the API doc, when a request failed, a description of the error is included in the answer. This function try to retrieve this description.
    ///
    /// - parameter data: Data sent back by the API.
    /// - returns: Return the error description if found in the data.
    private func parseErrorDescription(data : Any) -> String?{
        guard let json = data as? Dictionary<String, String>,
              let error = json["error"] else {
            return nil
        }
        return error
    }
}
