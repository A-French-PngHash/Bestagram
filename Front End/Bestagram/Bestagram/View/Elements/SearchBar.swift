//
//  SearchBar.swift
//  Bestagram
//
//  Created by Titouan Blossier on 01/01/2021.
//

import SwiftUI

struct SearchBar: View {

    var placeholder: String = ""
    var height: CGFloat = 40

    /// Input of the search bar.
    @Binding var input: String
    var onEdit : ((String) -> Void)? = nil

    var body: some View {
        HStack {
            Spacer()
                .frame(width: 10)
            Image(systemName: "magnifyingglass")
                .foregroundColor(BestagramApp.textGray)
            TextField(self.placeholder, text: $input)
                .foregroundColor(BestagramApp.textGray)
                .disableAutocorrection(true)
                .autocapitalization(.none)
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
        .frame(height: height)
        .background(BestagramApp.backgroundGray)
        .cornerRadius(10)
    }
}

struct SearchBar_Previews: PreviewProvider {
    @State static var input: String = ""

    static var previews: some View {
        SearchBar(placeholder: "Search for a person", input: $input, onEdit: { (_) in
        })
        .colorScheme(.dark)
        .font(ProximaNova(size: 21, bold: false).font)
    }
}
