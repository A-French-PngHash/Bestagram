//
//  Billabong.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/12/2020.
//

import SwiftUI

struct Billabong{
    /// Font object when the struct is instantiated.
    let font : Font

    init(size : CGFloat) {
        self.font = Font.custom("Billabong", size: size)
    }
}
