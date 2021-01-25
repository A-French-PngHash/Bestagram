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
    let image: UIImage
    @State var tags: Array<Tag> = []

    var imageTap: some Gesture {
        DragGesture(minimumDistance: 0, coordinateSpace: .local)
            .onEnded { (value) in
                // User has tapped the picture.
                let location = value.location

            }
    }

    var body: some View {
        VStack {
            TopBarView(trailingButtonText: "Done", titleText: "Tag People") {

            }
            Image(uiImage: image)
                .resizable()
                .frame(width: UIScreen.screenWidth, height: UIScreen.screenWidth, alignment: .center)
                .gesture(imageTap)

            Spacer()
            Text("Tap photo to tag people")
            Spacer()
        }
        .navigationBarHidden(true)
    }
}

struct TagPeopleView_Previews: PreviewProvider {
    static var previews: some View {
        TagPeopleView(image: BestagramApp.defaultPostPicture)
    }
}
