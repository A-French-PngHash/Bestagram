//
//  TagView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 30/01/2021.
//

import SwiftUI

/// View representing a single tag on a post.
struct TagView: View {
    var tag : Tag
    /// Total height of this view.
    ///
    /// Height of the triangle + height of the padding around the text + height of the text.
    static let height = Triangle.height + 7 * 2 + 21

    var text: some View {
        Text(tag.userTagged.username!)
            .foregroundColor(.white)
            .font(ProximaNova.bodyBold)
    }

    var body: some View {
        HStack {
            VStack {
                Triangle()
                    .opacity(0.7)
                    .foregroundColor(.black)
                ZStack {
                    RoundedRectangle(cornerRadius: 10)
                        .opacity(0.7)
                        .foregroundColor(.black)
                    text
                        .padding(.all, 7.0)
                }.fixedSize()
            }
        }
    }
}
struct Triangle: Shape {
    static let height : CGFloat = 10
    func path(in rect: CGRect) -> Path {
        var path = Path()
        let yOffset : CGFloat = 8
        path.move(to: CGPoint(x: rect.midX, y: rect.maxY + yOffset))
        path.addLine(to: CGPoint(x: rect.midX + 10, y: rect.maxY + yOffset))
        path.addLine(to: CGPoint(x: rect.midX, y: rect.maxY - Triangle.height / yOffset))
        path.addLine(to: CGPoint(x: rect.midX - 10, y: rect.maxY + yOffset))

        return path
    }
}

struct TagView_Previews: PreviewProvider {
    static var previews: some View {
        TagView(tag: Tag(userTagged: User(id: 3, username: "username", name: "myname"), position: [0, 0]))
    }
}
