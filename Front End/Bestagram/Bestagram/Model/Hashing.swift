//
//  Hashing.swift
//  Bestagram
//
//  Created by Titouan Blossier on 19/12/2020.
//

import Foundation
import CommonCrypto

class Hashing {
    static let shared = Hashing()
    private init() { }

    func pbkdf2(hash: CCPBKDFAlgorithm, password: String, saltData: Data, keyByteCount: Int, rounds: Int) -> Data? {
        guard let passwordData = password.data(using: .utf8) else { return nil }
        var derivedKeyData = Data(repeating: 0, count: keyByteCount)
        let derivedCount = derivedKeyData.count
        let derivationStatus: Int32 = derivedKeyData.withUnsafeMutableBytes { derivedKeyBytes in
            let keyBuffer: UnsafeMutablePointer<UInt8> =
                derivedKeyBytes.baseAddress!.assumingMemoryBound(to: UInt8.self)
            return saltData.withUnsafeBytes { saltBytes -> Int32 in
                let saltBuffer: UnsafePointer<UInt8> = saltBytes.baseAddress!.assumingMemoryBound(to: UInt8.self)
                return CCKeyDerivationPBKDF(
                    CCPBKDFAlgorithm(kCCPBKDF2),
                    password,
                    passwordData.count,
                    saltBuffer,
                    saltData.count,
                    hash,
                    UInt32(rounds),
                    keyBuffer,
                    derivedCount)
            }
        }
        return derivationStatus == kCCSuccess ? derivedKeyData : nil
    }

    // Converts data to a hexadecimal string
    func toHex(_ data: Data) -> String {
        return data.map { String(format: "%02x", $0) }.joined()
    }

    func pbkdf2sha256(password: String, salt: String, keyByteCount: Int, rounds: Int) -> Data {
        return pbkdf2(hash: CCPBKDFAlgorithm(kCCPRFHmacAlgSHA256), password: password, saltData: salt.data(using: .utf8)!, keyByteCount: keyByteCount, rounds: rounds)!
    }

    func hash(password: String, salt: String) -> String{
        return self.toHex(self.pbkdf2(hash: CCPBKDFAlgorithm(kCCPRFHmacAlgSHA256), password: password, saltData: salt.data(using: .utf8)!, keyByteCount: 32, rounds: 1000000)!)
    }
}
