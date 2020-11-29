//
//  PostView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/11/2020.
//

import SwiftUI

struct PostView: View {
    /// The photo posted. Contain information about the user, the number of like...
    let post: Post

    /// The distance the elements on the side of the screen should be from the screen
    let minSpaceFromEdge: CGFloat = 8

    var body: some View {
        VStack {
            HStack {
                Spacer()
                    .frame(width: minSpaceFromEdge)

                Image(uiImage: post.user.profilePicture)
                    .resizable()
                    .clipShape(Circle())
                    .frame(width: 30.0, height: 30.0)

                Text(post.user.username)
                    .foregroundColor(.black)
                    .font(ProximaNova.bodyBold)

                Spacer()
                Image(systemName: "ellipsis")
                Spacer()
                    .frame(width: minSpaceFromEdge)
            }
            Spacer()
                .frame(height: 8)
            Image(uiImage: post.image)
                .resizable()
                .frame(
                    width: UIScreen.main.bounds.width,
                    height: UIScreen.main.bounds.width)
            HStack {
                Spacer()
                    .frame(width: minSpaceFromEdge)
                Image(systemName: "heart")
                Spacer()
                    .frame(width: 13)
                Image(systemName: "bubble.right")
                Spacer()
                    .frame(width: 13)
                Image(systemName: "paperplane")
                Spacer()
                Image(systemName: "bookmark")
                Spacer()
                    .frame(width: minSpaceFromEdge)
            }
            Spacer()
                .frame(height: 5)
            HStack {
                Spacer()
                    .frame(width: minSpaceFromEdge)
                Text("Liked by \(post.numberOfLikes) persons")
                Spacer()
            }
            HStack {
                Spacer()
                    .frame(width: minSpaceFromEdge)
                DescriptionView(post: post)

                Spacer()
            }
            Spacer()
        }
        .font(ProximaNova.body)
    }
}

let defaultDescription = """
Twenty-five years ago, I published my first book,
The Road Ahead. At the time, people were wondering
where digital technology was headed and how it would
affect our lives, and I wanted to share my thoughts—and
my enthusiasm.

I had fun making some predictions about breakthroughs
in computing, and especially the Internet, that were
coming in the next couple of decades. You can find out
what I got right and what I got wrong at the link in my bio.
"""

let defaultUser = User(
    username: "thisisbillgates",
    followers: 329,
    numberOfPosts: 156,
    profilePicture: UIImage(named: "DefaultProfilePicture")!
)
let defaultPost = Post(
    user: defaultUser,
    image: UIImage(named: "DefaultPostPicture")!,
    numberOfLikes: 326,
    description: defaultDescription,
    postTime: Date(timeIntervalSinceNow: TimeInterval(-27653))
)

struct PostView_Previews: PreviewProvider {
    static var previews: some View {
        PostView(post: defaultPost)
            .previewDevice("iPhone 12 mini")
    }
}
