//
//  PictureSelectionView.swift
//  Bestagram
//
//  Created by Titouan Blossier on 27/12/2020.
//

import SwiftUI
import Photos

struct PictureSelectionView: View {
    @Environment(\.presentationMode) var presentationMode

    @ObservedObject var photos : PhotosModel = PhotosModel()
    @State var presentImagePicker: Bool = false

    /// Low quality selected image.
    @State var selectedImage: UIImage = UIImage()

    /// High quality loaded image.
    @State var loadedImage: UIImage = UIImage()
    /// Execute transition to next view
    @State var goNextView: Bool = false


    // TODO: - Implement this feature.
    /// When the user select a picture, if he does a certain gesture he can show more photo at once making it easier to select a picture.
    /// In this case the image currently selected is not displayed fully, it is shifted to the top.
    @State var displayFullImage: Bool = true

    /// User currently connected.
    var user : User

    var dragGesture: some Gesture {
        return DragGesture(minimumDistance: 80, coordinateSpace: .local)
            .onEnded { (gesture) in
                let xDist =  abs(gesture.location.x - gesture.startLocation.x)
                let yDist =  abs(gesture.location.y - gesture.startLocation.y)

                if gesture.startLocation.y < gesture.location.y && yDist > xDist {
                    // Down gesture
                } else if gesture.startLocation.y > gesture.location.y && yDist > xDist {
                    // Up gesture
                    displayFullImage = false
                }
            }
    }

    /// Apply the correct changes to select the image provided. (Load high def image)
    func selectImage(photo: UIImage) {
        // Check if the new selected image is the already selected image
        guard selectedImage != photo else {
            return
        }
        // The selected image variable is only modified here.
        selectedImage = photo
        // The loaded image variable is modified here and when the high quality image is loaded. This variable is the iamge shown in big.
        // Having two variables allow to find back which image is selected in the array of photo (previous if) and to display the high quality image without needing a third variable to indicate if the loading is finished.
        loadedImage = photo
        self.photos.getPhoto(index: photos.allPhotos.firstIndex(of: selectedImage)!, quality: 700) { (photo) in
            self.loadedImage = photo
        }
    }

    var imageScrollView: some View {
        HStack {
            let columns = [GridItem](repeating: GridItem(.flexible()), count: Int(UIScreen.screenWidth) / 80)
            let width = UIScreen.screenWidth / CGFloat(columns.count)
            ScrollView {
                LazyVGrid(columns: columns, content: {
                    ForEach(photos.allPhotos, id: \.self) { photo in
                        ZStack {
                            if selectedImage == photo {
                                Rectangle()
                                    .fill(Color.white)
                                    .frame(width: width, height: width)
                            }
                            Image(uiImage: photo)
                                .resizable()
                                .frame(width: width, height: width)
                                .aspectRatio(1, contentMode: .fit)
                                .onTapGesture {
                                    selectImage(photo: photo)
                                }
                                // If this image is the selected one we reduce its opacity in order to make appear the white background behing.
                                .opacity(selectedImage == photo ? 0.6 : 1)
                            //Color.orange.frame(width: width, height: width)
                        }

                    }
                })
            }
        }
        .gesture(dragGesture)
    }

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
                    if selectedImage != UIImage() && selectedImage != loadedImage {
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

            Image(uiImage: loadedImage)
                .resizable()
                .frame(width: UIScreen.screenWidth, height: UIScreen.screenWidth, alignment: .center)

            imageScrollView
            NavigationLink(
                destination: PostSettingView(postImage: loadedImage, user: self.user),
                isActive: $goNextView,
                label: {
                    EmptyView()
                })

            Spacer()
        }
        // Alert display if there was an error in the authorization of the access of the photo library.
        .alert(isPresented: .constant(self.photos.errorString != "") ) {
            Alert(title: Text("Error"), message: Text(self.photos.errorString ), dismissButton: Alert.Button.default(Text("OK")))
        }
        .onAppear(perform: {
            // Set the default selected image as the first one.
            photos.firstPhotoLoaded = { () in
                // Check if the user hasn't already selected another image.
                if self.selectedImage == UIImage() {
                    selectImage(photo: photos.allPhotos[0])
                }
            }
        })
        .navigationBarHidden(true)
    }
}

/// Class retrieving photos from the user's photo library.
class PhotosModel: ObservableObject {
    @Published var allPhotos = [UIImage]()
    @Published var errorString : String = ""
    var results : PHFetchResult<PHAsset>!
    let requestOptions = PHImageRequestOptions()
    let manager = PHImageManager.default()

    /// Closure called when the first photo is loaded in get all photos.
    var firstPhotoLoaded: (() -> Void)?

    init() {
        let fetchOptions = PHFetchOptions()
        fetchOptions.sortDescriptors = [NSSortDescriptor(key: "creationDate", ascending: false)]

        results = PHAsset.fetchAssets(with: .image, options: fetchOptions)

        PHPhotoLibrary.requestAuthorization { (status) in
            switch status {
            case .authorized:
                self.errorString = ""
                self.getAllPhotos()
            case .denied, .restricted:
                self.errorString = "Photo access permission denied"
            case .notDetermined:
                self.errorString = "Photo access permission not determined"
            case .limited:
                self.errorString = ""
                self.getAllPhotos()
            @unknown default:
                fatalError()
            }
        }
    }


    /// Get a specific photo from the phone's photo library.
    ///
    /// - parameter index: Index of the photo in the library.
    /// - parameter quality: Size in pixel of the side of the square photo.
    /// - parameter callback: Callback called when loading is finished.
    func getPhoto(index: Int, quality: Int, callback: @escaping (UIImage) -> Void) {
        let asset = results.object(at: index)
        let size = CGSize(width: quality, height: quality)
        manager.requestImage(for: asset, targetSize: size, contentMode: .aspectFill, options: requestOptions) { (image, _) in
            if let image = image {
                callback(image)
            } else {
                print("error fetching photo at index \(index)")
            }
        }
    }

    /// Retrieve all photo from the phone's photo library.
    ///
    /// - parameter firstImageLoaded: As soon as the first image is loaded, this closure is called.
    fileprivate func getAllPhotos() {
        requestOptions.isSynchronous = false
        requestOptions.deliveryMode = .highQualityFormat
        if results.count > 0 {
            for i in 0..<results.count {
                let asset = results.object(at: i)
                let size = CGSize(width: 80, height: 80)
                manager.requestImage(for: asset, targetSize: size, contentMode: .aspectFill, options: requestOptions) { (image, _) in
                    if let image = image {
                        self.allPhotos.append(image)
                        if self.allPhotos.count == 1 && self.firstPhotoLoaded != nil {
                            self.firstPhotoLoaded!()
                        }
                    } else {
                        print("error asset to image")
                    }
                }
            }
        } else {
            self.errorString = "No photos to display"
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
