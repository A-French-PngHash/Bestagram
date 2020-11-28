//
//  PostView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/11/2020.
//

import SwiftUI

struct PostView: View {
    /// The photo posted. Contain information about the user, the number of like...
    let postImage : Post
    
    /// The distance the elements on the side of the screen should be from the screen
    let minSpaceFromEdge : CGFloat = 8
    
    var body: some View {
        VStack {
            HStack {
                Spacer()
                    .frame(width: minSpaceFromEdge)
                    
                Image(uiImage: postImage.user.profilePicture)
                    .resizable()
                    .clipShape(Circle())
                    .frame(width: 30.0, height: 30.0)
                
                Text(postImage.user.username)
                
                Spacer()
                Image(systemName: "gearshape.fill")
                Spacer()
                    .frame(width: minSpaceFromEdge)
            }
            Spacer()
                .frame(height : 8)
            Image(uiImage: postImage.image)
                .resizable()
                .frame(width: UIScreen.main.bounds.width,
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
                .frame(height : 5)
            HStack {
                Spacer()
                    .frame(width: minSpaceFromEdge)
                Text("Liked by \(postImage.numberOfLikes) persons")
                Spacer()
            }
            Spacer()
        }
        .font(.custom("ProximaNova-Regular", size: 15))
    }
}


let defaultUser = User(username: "thisisbillgates", followers: 329, numberOfPosts: 156, profilePicture: UIImage(named: "DefaultProfilePicture")!)
let defaultPost = Post(user: defaultUser, image: UIImage(named: "DefaultPostPicture")!, numberOfLikes: 326)

struct PostView_Previews: PreviewProvider {
    
    
    static var previews: some View {
        PostView(postImage: defaultPost)
    }
}
