//
//  PickUsernameView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 21/01/2021.
//

import SwiftUI

/// Display a search bar, a keyboard and a list of username. Make call to the API.
struct PickUsernameView: View {

    /// Closure called when the user picked a username. Send the username as the first argument.
    var onPickedUsername : (String) -> Void
    /// Closure called when the user click the cancel button.
    var onCancelButtonPressed : () -> Void

    @State var searchInput : String = ""

    var body: some View {
        VStack {
            HStack {
                SearchBar(placeholder: "Search for a person", height: 30, input: $searchInput)
                    .padding(5)
                Button(action: {
                    onCancelButtonPressed()
                }, label: {
                    Text("Cancel")
                        .foregroundColor(.black)
                        .font(ProximaNova.init(size: 20, bold: false).font)
                })
                .padding(5)
            }
            Spacer()

        }
        .edgesIgnoringSafeArea(.all)

    }
}

struct PickUsernameView_Previews: PreviewProvider {
    static var previews: some View {
        PickUsernameView(
            onPickedUsername: {(_) in },
            onCancelButtonPressed: { }
        )
        .colorScheme(.dark)
        .font(ProximaNova.body)
    }
}
