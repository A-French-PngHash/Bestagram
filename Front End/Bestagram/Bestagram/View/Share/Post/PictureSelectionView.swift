//
//  PictureSelectionView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/12/2020.
//

import SwiftUI
import Photos
import PhotosUI

struct PictureSelectionView: View {
    @Environment(\.presentationMode) var presentationMode

    @State var presentImagePicker: Bool = false

    /// Selected image.
    @State var selectedImage: UIImage = UIImage(systemName: "photo.fill")!
    /// Execute transition to next view
    @State var goNextView: Bool = false

    /// User currently connected.
    var user : User

    var body: some View {
        VStack {
            ZStack {
                HStack {
                    Spacer()
                        .frame(width: 10)
                    Image(systemName: "xmark")
                        .font(.title)
                    Spacer()
                    // Show next button if the image isn't the default one and if the loaded image is the full size one.
                    if selectedImage != UIImage(systemName: "photo.fill")! {
                        Button(action: {
                            goNextView = true
                        }, label: {
                            Text("Next")
                                .font(ProximaNova.bodyBold)
                        })
                    } else if selectedImage != UIImage(){
                        ProgressView()
                    }
                    Spacer()
                        .frame(width: 10)
                }
                HStack {
                    Spacer()
                    Text("New Post")
                        .font(ProximaNova(size: 15, bold: true).font)
                    Spacer()
                }
            }

            Image(uiImage: selectedImage)
                .frame(width: UIScreen.screenWidth, height: UIScreen.screenWidth, alignment: .center)

            PhotoPicker(filter: .images, limit: 1) { (results) in
                PhotoPicker.convertToUIImageArray(fromResults: results) { (images, error) in
                    guard (error == nil) else {
                        print(error)
                        return
                    }
                    if let images = images, images.count > 0 {
                        self.selectedImage = images[0]
                    }
                }
            }

            NavigationLink(
                destination: PostSettingView(postImage:selectedImage, user: self.user),
                isActive: $goNextView,
                label: {
                    EmptyView()
                })

            Spacer()
        }
        .navigationBarHidden(true)
    }
}

struct PhotoPicker: UIViewControllerRepresentable {
    typealias UIViewControllerType = PHPickerViewController

    let filter: PHPickerFilter
    var limit: Int = 0 // 0 == 'no limit'.
    let onComplete: ([PHPickerResult]) -> Void

    func makeUIViewController(context: Context) -> PHPickerViewController {
        var configuration = PHPickerConfiguration()
        configuration.filter = filter
        configuration.selectionLimit = limit
        let controller = PHPickerViewController(configuration: configuration)

        controller.preferredContentSize = CGSize(width:400, height:200)
        controller.delegate = context.coordinator

        controller.navigationController?.setToolbarHidden(true, animated: false)
        controller.navigationController?.setNavigationBarHidden(true, animated: false)

        return controller
    }

    func updateUIViewController(_ uiViewController: PHPickerViewController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    class Coordinator: PHPickerViewControllerDelegate {

        func picker(_ picker: PHPickerViewController, didFinishPicking results: [PHPickerResult]) {
            parent.onComplete(results)
            picker.dismiss(animated: true)
        }

        private let parent: PhotoPicker

        init(_ parent: PhotoPicker) {
            self.parent = parent
        }
    }

    static func convertToUIImageArray(fromResults results: [PHPickerResult], onComplete: @escaping ([UIImage]?, Error?) -> Void) {
        var images = [UIImage]()

        let dispatchGroup = DispatchGroup()

        for result in results {
            dispatchGroup.enter()
            let itemProvider = result.itemProvider
            if itemProvider.canLoadObject(ofClass: UIImage.self) {
                itemProvider.loadObject(ofClass: UIImage.self) { (imageOrNil, errorOrNil) in
                    if let error = errorOrNil {
                        onComplete(nil, error)
                        dispatchGroup.leave()
                    }
                    if let image = imageOrNil as? UIImage {
                        images.append(image)
                        dispatchGroup.leave()
                    }
                }
            }
        }
        dispatchGroup.notify(queue: .main) {
            onComplete(images, nil)
        }
    }
}

struct PictureSelectionView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationView {
            PictureSelectionView(selectedImage: UIImage(systemName: "photo")!, user: testUser)
                .font(ProximaNova.body)
        }
    }
}
