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
    /// - Parameters:
    ///     - callback: Closure called when the API sent back the response.
    ///     - success : Wether the request succeeded or not.
    ///     - content: If the request succeeded then this contain the token. If the request failed then this contain the error documentation provided by the API.
    ///     - code: In case of a failure, is the error code.
    ///
    func fetchToken(username: String, password : String, callback : @escaping (_ success: Bool, _ content: String?, _ code: Int?) -> Void) {
        let parameters = ["username": username, "hash": password]
        Api.session.request(path + loginUrl, method: .get, parameters: parameters).responseJSON { (response) in
            debugPrint(response)
            switch response.result{
            case .failure(_):
                // Error happened in the request.
                callback(false, nil, response.response?.statusCode)
                return
            case .success(let data):
                guard response.error == nil && response.response?.statusCode == 200 else {
                    // Error happened in the request.
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
                callback(true, token, nil)
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
