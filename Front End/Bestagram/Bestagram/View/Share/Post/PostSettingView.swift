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
    /// Caption going with the post.
    @State var caption: String = "Write a caption..."
    let placeholderString: String = "Write a caption..."

    /// Display the view where the user can tag people on the photos.
    @State var displayTagView: Bool = false
    /// Tag the user want to set with the post.
    @State var tags : Array<Tag> = []

    /// User currently connected.
    var user : User

    var enterCaption: some View {
        HStack {
            
            Image(uiImage: postImage)
                .resizable()
                .frame(width: 50, height: 50, alignment: .leading)
                .padding(10)
            TextEditor(text: $caption)
                .frame(height: 60)
                .foregroundColor(caption == placeholderString ? .gray : .primary)
                .onTapGesture(perform: {
                    if caption == placeholderString {
                        self.caption = ""
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
                        .foregroundColor(.white)
                    Spacer()
                    Image(systemName: "chevron.right")
                        .foregroundColor(.white)
                    Spacer()
                        .frame(width: 10)
                }
            })
            NavigationLink(
                destination:
                    TagPeopleView(image: postImage, tags: tags, user: user, onUserIsDone : { (tags) in
                        self.displayTagView = false
                        self.tags = tags
                    }),
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
            TopBarView(presentationMode : presentationMode, trailingButtonText: "Share", titleText: "Create post") {
                //TODO: - When creating home view then link the press of this button to the view.
                user.getToken { (success, token, error) in
                    if let token = token, success {

                        ShareService.shared.createPost(token: token, image: self.postImage, caption: self.caption, tags: tags) { (success, error) in
                            if let err = error, success {
                                print("post did not suceeded")
                                print(err)
                            } else {
                                print("post suceeded")
                            }
                        }
                    }
                }
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
            PostSettingView(postImage: BestagramApp.previewPostPicture, user : testUser)
                .font(ProximaNova.body)
        }
    }
}
