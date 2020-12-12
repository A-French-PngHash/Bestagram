//
//  ProximaNova.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import SwiftUI

struct ProximaNova {
    static let body = Font.custom("ProximaNova-Regular", size: 15)
    static let bodyBold = Font.custom("ProximaNova-Bold", size: 15)

    /// Font when the class is instantiated.
    let font: Font

    init(size: CGFloat, bold: Bool) {
        font = Font.custom(bold ? "ProximaNova-Bold" : "ProximaNova-Regular", size: size)
    }
}
