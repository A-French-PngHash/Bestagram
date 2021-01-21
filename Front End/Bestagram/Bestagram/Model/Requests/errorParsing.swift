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
