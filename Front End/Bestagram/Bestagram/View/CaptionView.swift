//
//  CaptionView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/11/2020.
//

import SwiftUI

struct CaptionView: View {
    /// Define if the application should show the full caption for this post or the reduced.
    ///
    /// This variable is modified when the reduced caption is taped.
    @State var showFullCaption: Bool = false
    let post: Post

    var body: some View {
        if showFullCaption {
            (Text(post.user.username!)
                .font(ProximaNova.bodyBold)
            + Text(" " + post.caption.fullCaption)
                .font(ProximaNova.body))
                .transition(.opacity)
        } else {
            Button(action: {
                withAnimation(.linear(duration: 0.25), {
                    showFullCaption = true
                })
            }, label: {
                Text(post.user.username!)
                    .font(ProximaNova.bodyBold)
                + Text(" " + post.caption.reducedCaption)
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

struct CaptionView_Previews: PreviewProvider {
    static var previews: some View {
        CaptionView(post: defaultPost)
    }
}
