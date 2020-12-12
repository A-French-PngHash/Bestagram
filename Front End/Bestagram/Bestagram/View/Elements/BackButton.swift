//
//  BackButton.swift
//  Bestagram
//
//  Created by Titouan Blossier on 11/12/2020.
//

import SwiftUI

/// Back button to replace the default one in the nav bar.
struct BackButton: View {

    @Environment(\.colorScheme) var colorScheme
    var presentationMode: Binding<PresentationMode>! = nil

    var body: some View {
        Button(action: {
            presentationMode.wrappedValue.dismiss()
        }, label: {
            Image(systemName: "chevron.backward")
                .foregroundColor(colorScheme == .dark ? Color.white : Color.black)
        })
    }
}

struct BackButtonView_Previews: PreviewProvider {
    static var previews: some View {
        BackButton()
    }
}
