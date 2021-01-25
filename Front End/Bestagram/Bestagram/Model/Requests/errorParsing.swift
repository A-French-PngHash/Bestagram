//
//  errorParsing.swift
//  Bestagram
//
//  Created by Titouan Blossier on 21/01/2021.
//

import Foundation

/// According to the API doc, when a request failed, a description of the error is included in the answer. This function try to retrieve this description.
///
/// - parameter data: Data sent back by the API.
/// - returns: Return the error description if found in the data.
func parseErrorDescription(data : Any) -> String?{
    guard let json = data as? Dictionary<String, String>,
          let error = json["error"] else {
        return nil
    }
    return error
}

/// Parse an error from the json dictionary. This function assumes there **is** an error. If an error is not found it will send back UnknownError.
///
/// - parameter data: Data sent back by the API.
/// - returns: Return the error as a BestagramError.
func parseError(data: Any) -> BestagramError {
    let errorCodes : [Int: BestagramError] = [
        1: InvalidCredentials(),
        2: UsernameAlreadyTaken(),
        3: EmailAlreadyTaken(),
        4: InvalidEmail(),
        5: InvalidUsername(),
        6: InvalidName(),
        7: MissingInformations()
    ]
    guard let json = data as? Dictionary<String, Any>,
          let code = json["errorCode"] as? Int,
          let error = errorCodes[code] else {
        return UnknownError(documentation: "")
    }
    return error
}
