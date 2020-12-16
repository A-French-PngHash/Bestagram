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
            SignInOrUpChoiceView()
                .font(ProximaNova.body)
                .onAppear(perform: {
                    LoginService.shared.fetchToken(username: "titouan", password: "thisisahash") { (success, response, code) in
                        print("done")
                    }
                })
        }
    }
}
