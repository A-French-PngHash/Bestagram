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
    /// - parameter email: Email of the user, required only in case of a sign up.
    /// - parameter register: Wether to perform a sign up or sign in operation.
    /// - parameter name: Name of the user, required only in case of a sign up.
    /// - Parameters:
    ///     - callback: Closure called when the API sent back the response.
    ///     - success : Wether the request succeeded or not.
    ///     - token: Token of the user.
    ///     - expirationDate: Date at which the token will be expired and a new one will be needed.
    ///     - error: If the request did not suceed then this the error corresponding.
    ///
    func fetchToken(
        username: String,
        password : String,
        email : String = "",
        register : Bool,
        name: String = "",
        callback : @escaping (_ success: Bool,
                              _ token: String?,
                              _ expirationDate: Date?,
                              _ error: BestagramError?) -> Void) {
        var parameters = ["username": username, "hash": password]

        // The main difference between the user being logged in/registered is the method used.
        var method : HTTPMethod = .get
        if register {
            method = .put
            parameters["email"] = email
            parameters["name"] = name
            // These two parameters are required in case of a sign up.
        }

        Api.session.request(path + loginUrl, method: method, parameters: parameters).responseJSON { (response) in

            switch response.result{
            case .failure(_):
                // Error happened BEFORE the request. In this case the request never reached the server.
                callback(false, nil, nil,  ConnectionError())
                return

            case .success(let data):
                guard let json = data as? Dictionary<String, Any>,
                      let success = json["success"] as? Bool,
                      let strDate = json["date"] as? String,
                      let expirationDate = self.getDateFromString(strDate: strDate) else {
                    callback(false, nil, nil,  UnknownError(documentation: "Invalid json response."))
                    return
                }
                guard let token = json["token"] as? String, success else {
                    callback(false, nil, nil, parseError(data: data))
                    return
                }
                callback(true, token, expirationDate, nil)
            }
        }
    }

    /// When the token is sent from the api, its expiration date is sent along as a string. This method allow us to parse this string to a date again.
    func getDateFromString(strDate: String) -> Date?{
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "y-M-d HH:mm:ss"
        let date = dateFormatter.date(from: strDate)
        return date
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
}
