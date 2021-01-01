//
//  PostSettingView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/12/2020.
//

import SwiftUI

struct PostSettingView: View {

    @Environment(\.presentationMode) var presentationMode

    /// Image chosen by the user to be the content of what will be posted.
    let postImage : UIImage
    /// Description going with the post.
    @State var description: String = "Write a caption..."
    let placeholderString: String = "Write a caption..."

    /// Display the view where the user can tag people on the photos.
    @State var displayTagView: Bool = false

    var enterCaption: some View {
        HStack {
            
            Image(uiImage: postImage)
                .resizable()
                .frame(width: 50, height: 50, alignment: .leading)
                .padding(10)
            TextEditor(text: $description)
                .frame(height: 60)
                .foregroundColor(description == placeholderString ? .gray : .primary)
                .onTapGesture(perform: {
                    if description == placeholderString {
                        description = ""
                    }
                })
        }
    }

    var tagPeople: some View {
        HStack {
            Button(action: {
                displayTagView = true
            }, label: {
                HStack {
                    Spacer()
                        .frame(width: 10)
                    Text("Tag people")
                        .foregroundColor(.black)
                    Spacer()
                    Image(systemName: "chevron.right")
                        .foregroundColor(.black)
                    Spacer()
                        .frame(width: 10)
                }
            })
            NavigationLink(
                destination: TagPeopleView(image: postImage),
                isActive: $displayTagView,
                label: {
                    EmptyView()
                })
        }
    }

    var addLocation: some View {
        Button(action: {

        }, label: {
            HStack {
                Spacer()
                    .frame(width: 10)
                Text("Add Location")
                Spacer()
                Image(systemName: "chevron.right")
                Spacer()
                    .frame(width: 10)
            }
        })
    }

    var body: some View {
        VStack {
            TopBarView(trailingButtonText: "Next", titleText: "Create post") {
                print("button press")
            }
            Divider()
            enterCaption
            Divider()
            tagPeople
            Divider()


            Spacer()
        }
        .navigationBarHidden(true)
    }
}

struct PostSettingView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            PostSettingView(postImage: UIImage(systemName: "photo")!)
                .font(ProximaNova.body)
        }
    }
}
