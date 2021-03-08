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

    let loginUrl = "user/login/%@"
    let refreshLoginUrl = "user/login/refresh/%@"
    let checkEmailTakenUrl = "email/%@/taken"


    /// Only use this method if the refresh token has not been fetched yet.
    func login(username: String, password: String, callback : @escaping (_ success: Bool, _ token: String?, _ expirationDate: Date?, _ refreshToken: String?, _ error: BestagramError?) -> Void) {
        fetchToken(username: username, password: password, register: false, callback: callback)
    }

    func signup(username: String, password : String, email : String, name: String, callback : @escaping (_ success: Bool, _ token: String?, _ expirationDate: Date?, _ refreshToken: String?, _ error: BestagramError?) -> Void) {
        fetchToken(username: username, password: password, email: email, register: true, name: name, callback: callback)
    }

    /// Makes use of the refresh 
    func refreshLogin(refreshToken : String, callback : @escaping (_ success: Bool, _ token: String?, _ expirationDate: Date?, _ refreshToken: String?, _ error: BestagramError?) -> Void) {
        fetchToken(refresh: true, refreshToken: refreshToken, callback: callback)
    }

    //MARK: - Functions
    /// Fetch the token using the Bestagram API. Have the option of creating the user.
    ///
    /// - parameter username: Username to use.
    /// - parameter password: **Encrypted** password. Encrypted as indicated in the API Documentation.
    /// - parameter email: Email of the user, required only in case of a sign up.
    /// - parameter register: Wether to perform a sign up or sign in operation.
    /// - parameter refresh: Login via the refresh token.
    /// - parameter refreshToken: Refresh token. Must be provided if refresh is set to true.
    /// - parameter name: Name of the user, required only in case of a sign up.
    /// - Parameters:
    ///     - callback: Closure called when the API sent back the response.
    ///     - success : Wether the request succeeded or not.
    ///     - token: Token of the user.
    ///     - expirationDate: Date at which the token will be expired and a new one will be needed.
    ///     - refreshToken: Refresh token.
    ///     - error: If the request did not suceed then this the error corresponding.
    ///
    func fetchToken(
        username: String = "",
        password : String = "",
        email : String = "",
        register : Bool = false,
        refresh : Bool = false,
        refreshToken : String = "",
        name: String = "",
        callback : @escaping (_ success: Bool,
                              _ token: String?,
                              _ expirationDate: Date?,
                              _ refreshToken: String?,
                              _ error: BestagramError?) -> Void) {
        var parameters : Dictionary<String, String> = [:]
        var fullUrl = ""
        var method : HTTPMethod = .post

        if refresh { // Login using refresh token.
            fullUrl = path + String(format: refreshLoginUrl, refreshToken)
        } else { // Login using credentials.
            fullUrl = path + String(format: loginUrl, username)
            parameters = ["hash": password]
            if register {
                method = .put
                parameters["email"] = email
                parameters["name"] = name
                // These two parameters are required in case of a sign up.
            }
        }


        Api.session.request(fullUrl, method: method, parameters: parameters).responseJSON { (response) in

            switch response.result{
            case .failure(_):
                // Error happened BEFORE the request. In this case the request never reached the server.
                callback(false, nil, nil, nil, BestagramError.ConnectionError)
                return

            case .success(let data):
                guard let json = data as? Dictionary<String, Any>,
                      let success = json["success"] as? Bool else {
                    callback(false, nil, nil, nil, BestagramError.InvalidJson)
                    return
                }
                guard let token = json["token"] as? String,
                      let strDate = json["token_expiration_date"] as? String,
                      let expirationDate = self.getDateFromString(strDate: strDate), success else {
                    callback(false, nil, nil, nil, parseError(data: data))
                    return
                }
                var refreshToken : String?
                if !refresh {
                    // The refresh token is in the response only if the authentication wasn't made using the refresh token.
                    // e.g. authentication by credentials/signup with credentials.
                    guard let refreshTok = json["refresh_token"] as? String else {
                        callback(false, nil, nil, nil, parseError(data: data))
                        return
                    }
                    refreshToken = refreshTok
                }
                callback(true, token, expirationDate, refreshToken, nil)
            }
        }
    }

    /// When the token is sent from the api, its expiration date is sent along as a string. This method allow us to parse this string to a date
    /// again.
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
        let fullUrl = path + String(format: checkEmailTakenUrl, email)
        Api.session.request(fullUrl, method: .get).responseJSON { (response) in
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
