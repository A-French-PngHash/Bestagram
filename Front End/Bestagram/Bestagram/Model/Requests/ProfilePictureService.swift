//
//  ProfilePictureService.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/03/2021.
//

import UIKit
import Alamofire

class ProfilePictureService {
    //MARK: - Singleton
    static let shared = ProfilePictureService()
    private init() { }

    //MARK: - Urls
    let path = Api.path

    let profilePictureUrl = "user/%@/profile/picture"

    func getProfilePicture(id : Int, callback : @escaping (_ success : Bool, _ image : UIImage?, _ error : BestagramError?) -> Void) {
        let fullUrl = path + String(format: profilePictureUrl, String(id))

        Api.session.request(fullUrl).responseImage { (response) in
            if case .success(let image) = response.result {
                callback(true, image, nil)
            } else {
                callback(false, nil, .ConnectionError)
            }
        }
    }
}
