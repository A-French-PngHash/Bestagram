//
//  InterfacePositioningView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 25/12/2020.
//

import SwiftUI

/// Take some view as parameter and apply effects to it.
/// It positione the view in the center with a distance to the edge.
/// It adds a back button.
struct InterfacePositioningView<Content: View>: View {

    @Environment(\.presentationMode) var presentationMode
    let content: Content
    let showBackButton : Bool
    @State var alreadyHaveAnAccount: Bool = false
    @State var dontHaveAnAccount: Bool = false

    /// Initializer for this view.
    ///
    /// - parameter showBackButton: Wether to show the back button at the top of the view or not.
    /// - parameter alreadyHaveAnAccount: If set to true, will show the already have an account view at the bottom.
    /// - parameter dontHaveAnAccount: If set to true, will show the dont have an account view at the bottom.
    /// - parameter content: Content to put in the middle of the screen between the formating.
    init(showBackButton: Bool = true, alreadyHaveAnAccount: Bool = false, dontHaveAnAccount: Bool = true, @ViewBuilder content: @escaping () -> Content) {
        self.showBackButton = showBackButton
        self.content = content()
        self.alreadyHaveAnAccount = alreadyHaveAnAccount
        self.dontHaveAnAccount = dontHaveAnAccount
    }

    var body: some View {
        VStack {
            if showBackButton {
                HStack {
                    Spacer()
                        .frame(width: 10)
                    BackButton(presentationMode: presentationMode)
                    Spacer()
                }
            }
            HStack {
                Spacer()
                    .frame(width: 15)
                content
                Spacer()
                    .frame(width: 15)
            }
            Spacer()
            if alreadyHaveAnAccount {
                AlreadyHaveAccountView()
            } else if dontHaveAnAccount {
                DontHaveAccountView()
            }
        }
    }
}


struct InterfacePositioningView_Previews: PreviewProvider {
    static var previews: some View {
        InterfacePositioningView {
            Text("test")
        }
    }
}
