//
//  ProximaNova.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import SwiftUI

/// Struct providing easy access for use to the ProximaNova font installed.
struct ProximaNova {
    // The thin version rather than the regular is used for the body.
    static let body = Font.custom("Proxima Nova Regular", size: 17)
    static let bodyBold = Font.custom("Proxima Nova Bold", size: 17)

    /// Font object when the struct is instantiated.
    let font: Font

    init(size: CGFloat, bold: Bool) {
        font = Font.custom(bold ? "Proxima Nova Bold" : "Proxima Nova Regular", size: size)
    }
}
