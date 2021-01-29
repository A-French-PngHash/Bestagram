//
//  StringProtocolExtension.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import Foundation

/// Extension used to acces a string character from a int index.
///     myString = "test"
///     print(myString[2])
/// Prints "s"
extension StringProtocol {
    subscript(offset: Int) -> Character {
        self[index(startIndex, offsetBy: offset)]
    }
}
