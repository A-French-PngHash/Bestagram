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
    static let body = Font.custom("ProximaNova-Thin.otf", size: 17)
    static let bodyBold = Font.custom("ProximaNova-Bold.otf", size: 17)

    /// Font object when the struct is instantiated.
    let font: Font

    init(size: CGFloat, bold: Bool) {
        font = Font.custom(bold ? "ProximaNova-Bold" : "ProximaNova-Thin", size: size)
    }
}
