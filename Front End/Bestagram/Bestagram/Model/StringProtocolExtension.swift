//
//  StringProtocolExtension.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import Foundation

extension StringProtocol {
    subscript(offset: Int) -> Character {
        self[index(startIndex, offsetBy: offset)]
    }
}
