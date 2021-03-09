//
//  TagPeopleView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/12/2020.
//

import SwiftUI

/// View where the user can add tagged people on his post.
struct TagPeopleView: View {

    @Environment(\.presentationMode) var presentationMode
    /// Post's image.
    let image: UIImage
    /// List of tag currently set by the user.
    @State var tags: Array<Tag>

    /// Wether or not to show the view asking for a username. This follows a tap on the image.
    @State private var showPickUsernameView : Bool = false
    @State private var lastTapLocation : Array<Float> = []

    /// User currently connected.
    var user : User

    /// Closure called when the user has finished adding tag to the photo.
    let onUserIsDone : (Array<Tag>) -> Void

    var body: some View {
        VStack {
            TopBarView(
                trailingButtonText: "Done",
                titleText: "Tag People",
                onTrailingButtonPress:  {
                    onUserIsDone(tags)
                    self.presentationMode.wrappedValue.dismiss()
                }, shouldShowBackButton: false)
            ZStack {
                Image(uiImage: image)
                    .resizable()
                    .frame(width: UIScreen.screenWidth, height: UIScreen.screenWidth, alignment: .center)
                    .onTapWithLocation() { (location) in
                        // The image takes all the screen width and is a square so we can be sure that both side in pixel are equal to the screen width.
                        // Relative to the top left corner of the image.
                        lastTapLocation = [
                            Float(location.x / UIScreen.screenWidth),
                            Float(location.y / UIScreen.screenWidth)
                        ]
                        withAnimation {
                            showPickUsernameView = true
                        }
                    }
                ForEach(0..<tags.count, id: \.self) { (index) in

                    TagView(tag: tags[index])
                        .position(
                            x: UIScreen.screenWidth * CGFloat(tags[index].position[0]),
                            y: (UIScreen.screenWidth * CGFloat(tags[index].position[1])) - (UIScreen.screenWidth / 2) + TagView.height)
                }
            }
            .fixedSize()

            Spacer()
            Text("Tap photo to tag people")
            Spacer()

            NavigationLink(
                destination:
                    PickUserView(onUserPicked: { (user) in
                        /// Removing duplicates.
                        var index = tags.firstIndex { (tag) -> Bool in
                            return tag.userTagged == user
                        }
                        while index != nil {
                            tags.remove(at: index!)
                            index = tags.firstIndex { (tag) -> Bool in
                                return tag.userTagged == user
                            }
                        }

                        tags.append(Tag(userTagged: user, position: self.lastTapLocation))
                        showPickUsernameView = false
                    }, onCancelButtonPressed: {
                        showPickUsernameView = false
                    }, user: user),
                isActive: $showPickUsernameView,
                label: {
                    EmptyView()
            })
                .transition(.opacity)

        }
        .navigationBarHidden(true)
    }
}

struct TagPeopleView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            TagPeopleView(image: BestagramApp.defaultPostPicture, tags: [], user: testUser) { (tags) in
                print(tags)
            }
        }
        .preferredColorScheme(.dark)
        .previewDevice("iPhone 12 Pro Max")
    }
}
