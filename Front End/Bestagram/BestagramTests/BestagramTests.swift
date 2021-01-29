//
//  BestagramTests.swift
//  BestagramTests
//
//  Created by Titouan Blossier on 27/11/2020.
//

import XCTest
import Foundation
import Alamofire
@testable import Bestagram

class BestagramTests: XCTestCase {
    override func setUp() {
    }

    // MARK: - Error parsing test
    func testGivenInvalidJsonWhenParsingErrorThenIsInvalidJsonError() {
        // Given invalid json.
        let invalidJson = "invalid".data(using: .utf8)

        // When parsing error.
        let error = parseError(data: invalidJson)

        // Then is invalid json error.
        XCTAssertEqual(error, BestagramError.InvalidJson)
    }

    func testGivenValidJsonWhenParsingErrorThenIsCorrectError() {
        for (code, error) in Api.errorCodes {
            let dic : NSDictionary = ["success": false, "errorCode": code]
            let jsonData = try! JSONSerialization.data(withJSONObject: dic)
            let decoded = try! JSONSerialization.jsonObject(with: jsonData, options: [])

            let errorParsed = parseError(data: decoded)

            XCTAssertEqual(error, errorParsed)
        }
    }
}
