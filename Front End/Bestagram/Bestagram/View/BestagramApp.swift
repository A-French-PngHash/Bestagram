//
//  BestagramApp.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/11/2020.
//

import SwiftUI

@main
struct BestagramApp: App {
    var body: some Scene {
        WindowGroup {
            PostView(post: defaultPost)
        }
    }
}
