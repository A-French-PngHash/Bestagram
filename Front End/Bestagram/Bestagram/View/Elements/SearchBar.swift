//
//  SearchBar.swift
//  Bestagram
//
//  Created by Titouan Blossier on 01/01/2021.
//

import SwiftUI

struct SearchBar: View {

    var placeholder: String = ""
    var onEdit : ((String) -> Void)? = nil

    /// Input of the search bar.
    @Binding var input: String

    var body: some View {
        HStack {
            Spacer()
                .frame(width: 10)
            Image(systemName: "magnifyingglass")
                .foregroundColor(BestagramApp.textGray)
            TextField(self.placeholder, text: $input)
                .foregroundColor(BestagramApp.textGray)
                .onChange(of: input, perform: { value in
                    if let edit = onEdit {
                        edit(value)
                    }
                })

            if input != "" {
                Button(action: {
                    input = ""
                }, label: {
                    Image(systemName: "delete.left")
                        .foregroundColor(BestagramApp.textGray)
                })
            }
            Spacer()
                .frame(width: 10)
        }
        .frame(height: 40.0)
        .background(BestagramApp.backgroundGray)
        .cornerRadius(10)
    }
}

struct SearchBar_Previews: PreviewProvider {
    @State static var input: String = ""

    static var previews: some View {
        SearchBar(placeholder: "Search for a person", onEdit: { (_) in
        }, input: $input)
        .colorScheme(.dark)
        .font(ProximaNova(size: 21, bold: false).font)
    }
}
