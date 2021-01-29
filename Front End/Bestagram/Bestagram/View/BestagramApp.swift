//
//  BestagramApp.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/11/2020.
//

import SwiftUI
import Cache

@main
struct BestagramApp: App {
    /// Background color to use on dark theme on elements like text field to distinguish with the black background.
    static public var backgroundGray = Color(red: 93/255, green: 92/255, blue: 93/255, opacity: 1)
    /// Text color to use when on dark mode.
    static public var textGray = Color(red: 127/255, green: 126/255, blue: 128/255, opacity: 1)
    /// Post picture to show in previews.
    static public var defaultPostPicture = UIImage(named: "DefaultPostPicture")!

    static public var allowedUsernameCharacters = "abcdefghijklmnopqrstuvwxyz0123456789_."
    
    var body: some Scene {
        WindowGroup {
            SearchPeopleView()
            /*
            SignInOrUpChoiceView()
                .font(ProximaNova.body)
                .colorScheme(.dark)
 */
        }
    }
}
