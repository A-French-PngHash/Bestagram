//
//  ErrorView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 29/01/2021.
//

import SwiftUI

/// View displayed when an error occured
struct ErrorView: View {

    /// Error text to be displayed in this view.
    var errorText: String
    var body: some View {
        HStack {
            Spacer()
                .frame(width: 10)
            Image(systemName: "exclamationmark.triangle")
            Text(errorText)
            Spacer()
        }
        .padding(.vertical, 10.0)
        .background(Color.gray)
        .cornerRadius(10)
    }
}

struct ErrorView_Previews: PreviewProvider {
    static var previews: some View {
        ErrorView(errorText: "Couldn't load search results")
    }
}
