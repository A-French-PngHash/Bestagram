//
//  testView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 28/12/2020.
//

import SwiftUI
import Photos

struct ContentView: View {
    @ObservedObject var photos = PhotosModel()
    var body: some View {
        List(photos.allPhotos, id: \.self) { photo in
            Image(uiImage: photo)
                .resizable()
                .frame(width: 200, height: 200, alignment: .center)
                .aspectRatio(1, contentMode: .fit)
        }
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
