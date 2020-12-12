//
//  DescriptionView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import SwiftUI

struct DescriptionView: View {
    /// Define if the application should show the full description for this post or the reduced.
    ///
    /// This variable is modified when the reduced description is taped.
    @State var showFullDescription: Bool = false
    let post: Post

    var body: some View {
        if showFullDescription {
            (Text(post.user.username)
                .font(ProximaNova.bodyBold)
            + Text(" " + post.description.fullDescription)
                .font(ProximaNova.body))
                .transition(.opacity)
        } else {
            Button(action: {
                withAnimation(.linear(duration: 0.25), {
                    showFullDescription = true
                })
            }, label: {
                Text(post.user.username)
                    .font(ProximaNova.bodyBold)
                + Text(" " + post.description.reducedDescription)
                + Text("... ")
                + Text("more")
                    .foregroundColor(.gray)
            })
            .foregroundColor(.black)
            .font(ProximaNova.body)
            .transition(.opacity)
        }
    }
}

struct DescriptionView_Previews: PreviewProvider {
    static var previews: some View {
        DescriptionView(post: defaultPost)
    }
}
