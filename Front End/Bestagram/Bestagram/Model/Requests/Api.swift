//
//  Api.swift
//  Bestagram
//
//  Created by Titouan Blossier on 13/12/2020.
//

import Foundation
import Alamofire

/// Provide usefull feature for connecting to the database.
class Api {
    /// This is the path leading to the API. It can be hosted at different location so this is why this file is untracked.
    /// If you haven't modify it, it should have the default path used by default by the API.
    static let path = "https://0.0.0.0:5002/"
    /// This manager is used to allow connection to self signed certificates.
    static let manager = ServerTrustManager(evaluators: ["0.0.0.0": DisabledTrustEvaluator()])
    /// Session used to make requests.
    static var session = Session(serverTrustManager: manager)

    static let errorCodes : [Int:BestagramError] = [
        1: BestagramError.InvalidCredentials,
        2: BestagramError.UsernameAlreadyTaken,
        3: BestagramError.EmailAlreadyTaken,
        4: BestagramError.InvalidEmail,
        5: BestagramError.InvalidUsername,
        6: BestagramError.InvalidName,
        7: BestagramError.MissingInformations
    ]
}
