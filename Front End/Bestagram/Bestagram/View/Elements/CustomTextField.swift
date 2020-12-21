//
//  CustomTextField.swift
//  Bestagram
//
//  Created by Titouan Blossier on 09/12/2020.
//

import SwiftUI

/// A Text field to enter text with additional element (like a cross to delete everything) and with premade style.
struct CustomTextField: View {

    // MARK: - Variables
    @Environment(\.colorScheme) var colorScheme

    /// Define if the programm should display a
    /// cross at the end of the text field to erase everything.
    var displayCross: Bool = true
    /// Define if dot should be displayed when the user enter text to hide what is entered.
    /// Mainly used for password.
    var secureEntry : Bool = false
    /// Placeholder to display in the text field.
    var placeholder: String
    /// The distance that should be from the length of the screen on each side of the text field.
    var distanceEdge: CGFloat = 0

    /// Input entered by user in the field.
    @Binding var input: String
    /// Indicate if the text field should have an error style.
    @Binding var error : Bool

    /// Action to perform when the text field is edited.
    var onEdit: ((String) -> Void)?

    let backgroundColorDarkMode: Color = Color(red: 11/255.0, green: 12/255.0, blue: 12/255.0, opacity: 1)
    let backgroundColorLightMode: Color = Color(red: 250/255.0, green: 250/255.0, blue: 250/255.0, opacity: 1)

    // MARK: - Body
    var body: some View {
        HStack {
            Spacer()
                .frame(width: distanceEdge)
            HStack {
                if secureEntry {
                    SecureField(self.placeholder, text: $input)
                        .onChange(of: input, perform: { value in
                            if let edit = onEdit {
                                edit(value)
                            }
                        })
                } else {
                    TextField(self.placeholder, text: $input)
                        .onChange(of: input, perform: { value in
                            if let edit = onEdit {
                                edit(value)
                            }
                        })
                }
                // Shows the cross or not.
                if displayCross && input != ""{
                    Button(action: {
                        self.input = ""
                    }, label: {
                        Image(systemName: "delete.left")
                    })
                }
            }
            .frame(height: 5)
            .padding()
            .background(self.colorScheme == ColorScheme.dark ? backgroundColorDarkMode : backgroundColorLightMode)
            .overlay(
                RoundedRectangle(cornerRadius: 4)
                    .stroke(error ? Color.red : Color.gray, lineWidth: 0.3)
            )

            Spacer()
                .frame(width: distanceEdge)
        }
    }
}

// MARK: - Preview

struct TextField_Previews: PreviewProvider {
    @State static var input: String = ""
    @State static var error : Bool = true

    static var previews: some View {
        CustomTextField(displayCross: true, placeholder: "email", distanceEdge: 20, input: $input, error: $error, onEdit: { (_) in

        })
            .preferredColorScheme(.dark)
    }
}
