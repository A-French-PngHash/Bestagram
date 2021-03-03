//
//  ShareService.swift
//  Bestagram
//
//  Created by Titouan Blossier on 30/01/2021.
//

import Foundation
import UIKit
import Alamofire
import AlamofireImage

/// This service provide tools to post a post to the api.
class ShareService {
    //MARK: - Singleton
    static let shared = ShareService()
    private init() { }

    //MARK: - Urls
    let path = Api.path

    let postUrl = "post"

    /// Register a new post by contacting the api.
    ///
    /// - parameter token: Token to connect to the api.
    /// - parameter image: Post's image.
    /// - parameter caption: Post's caption
    ///
    func createPost(token: String, image: UIImage, caption: String?, tags: Array<Tag>?, callback: @escaping (_ success : Bool, _ error : BestagramError?) -> Void) {
        var parameters : Dictionary<String, Any> = [:]

        let headers: HTTPHeaders = ["Authorization" : token]
        let method : HTTPMethod = .put

        if let caption = caption {
            parameters["caption"] = caption
        }

        var tagDictionary : Dictionary<String, Dictionary<String, Any>> = [:]
        if let tags = tags {
            for (index, element) in tags.enumerated() {
                tagDictionary[String(index)] = element.encodeJson()
            }
        }
        let jsonTagData = try! JSONSerialization.data(withJSONObject: tagDictionary)

        /*
         When I was implementing this part I had severals problem.
         My request was quite complex, I needed to upload an image, a normal request parameter (caption) and a json dictionary(tags).
         It meant that I had to use MultipartFormData. The use of it was quite hard to set up as I didn't find any good documentation.
        */

        let multipartFormData = MultipartFormData()
        for (key, value) in parameters {
            if "\(value)" == "[:]" { // Empty dictionary. Causes problem if sent over as [:] so we sent it over as []
                multipartFormData.append("[]".data(using: .utf8)!, withName: key as String)
            } else {
                multipartFormData.append("\(value)".data(using: .utf8)!, withName: key as String)
            }
        }
        let resizedImage = image.makeResizedImage(sideLength: BestagramApp.defaultImageSideLength)!
        multipartFormData.append(jsonTagData, withName: "tag")
        multipartFormData.append(resizedImage.pngData()!, withName: "image", fileName: "file.png", mimeType: "image/png")


        Api.session.upload(multipartFormData: multipartFormData, to: path + postUrl, method: method, headers: headers, fileManager: .default).responseJSON { (response) in
            switch response.result {
            case .failure(_):
                // Error happened BEFORE the request. In this case the request never reached the server.
                callback(false, BestagramError.ConnectionError)
                return
            case .success(let data):
                guard let json = data as? NSDictionary,
                      let success = json["success"] as? Bool else {
                    callback(false, BestagramError.InvalidJson)
                    return
                }

                guard success else {
                    callback(false, parseError(data: data))
                    return
                }
                callback(true, nil)
            }
        }
    }
}
