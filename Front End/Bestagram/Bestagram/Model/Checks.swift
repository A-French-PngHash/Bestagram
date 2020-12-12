//
//  Checks.swift
//  Bestagram
//
//  Created by Titouan Blossier on 11/12/2020.
//

import Foundation

class Checks {
    /// This class contain static functions which proceeds to checks on given inputs.

    static func isEmailValid(email: String) -> Bool {
        let pattern = """
        ^[a-zA-Z0-9\\.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$
        """

        //swiftlint:disable:next force_try
        let regex = try! NSRegularExpression(pattern: pattern)
        let range = NSRange(location: 0, length: email.utf16.count)
        let valid = regex.firstMatch(in: email.lowercased(), options: [], range: range) != nil
        return valid
    }
}
