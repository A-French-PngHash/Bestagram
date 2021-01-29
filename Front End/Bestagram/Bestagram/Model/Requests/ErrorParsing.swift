//
//  ErrorParsing.swift
//  Bestagram
//
//  Created by Titouan Blossier on 21/01/2021.
//

import Foundation

/// Parse an error from the json dictionary. This function assumes there **is** an error. If an error is not found it will send back UnknownError.
///
/// - parameter data: Data sent back by the API.
/// - returns: Return the error as a BestagramError.
func parseError(data: Any) -> BestagramError {
    guard let json = data as? NSDictionary,
          let code = json["errorCode"] as? Int,
          let error = Api.errorCodes[code] else {
        return BestagramError.InvalidJson
    }
    return error
}
