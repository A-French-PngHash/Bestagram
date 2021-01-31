//
//  TopBarView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/12/2020.
//

import SwiftUI

struct TopBarView: View {

    var presentationMode: Binding<PresentationMode>! = nil
    var trailingButtonText: String
    var titleText: String
    /// Called when trailing button is pressed.
    var onTrailingButtonPress: () -> Void

    /// Wheter or not to show the arrow pointing back.
    var shouldShowBackButton : Bool = true

    var body: some View {
        HStack {
            ZStack {
                HStack {
                    Spacer()
                        .frame(width: 10)
                    if shouldShowBackButton {
                        BackButton(presentationMode: presentationMode)
                            .font(ProximaNova(size: 14, bold: true).font)
                    }
                    Spacer()
                    Button(action : {
                        onTrailingButtonPress()
                    }, label: {
                        Text(trailingButtonText)
                            .font(ProximaNova(size: 17, bold: true).font)
                    })
                    Spacer()
                        .frame(width: 10)
                }
                HStack {
                    Spacer()
                    Text(titleText)
                    Spacer()
                }
            }
        }
    }
}

struct TopBarView_Previews: PreviewProvider {
    static var previews: some View {
        TopBarView(trailingButtonText: "done", titleText: "new post") { }
            .font(ProximaNova.body)
    }
}
