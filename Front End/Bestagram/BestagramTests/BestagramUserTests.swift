//
//  BestagramUserTests.swift
//  BestagramTests
//
//  Created by Titouan Blossier on 26/12/2020.
//

import XCTest
@testable import Bestagram


/// Tests regarding the user class.
class BestagramUserTests: XCTestCase {

    //MARK: - Username from email test
    func testGivenCorrectEmailWhenGettingUsernameThenIsWhatPreceedTheAtSign() {
        // Given correct email.
        let email = "bestagram.test@bestagram.com"
        let wantedUsername = "bestagram.test"

        // When getting username.
        var username = ""
        do {
            username = try User.usernameFromEmail(email: email)
        } catch {
            print(error)
            XCTAssertTrue(false)
        }

        // Then is what preceed the at sign.
        XCTAssertEqual(username, wantedUsername)
    }

    func testGivenIncorrectEmailWhenGettingUsernameThenThrowError() {
        // Given incorrect email. (without @ sign)
        let email = "bestagram.testbestagram.com"

        // When getting username.
        var errorHappenned = false
        do {
            _ = try User.usernameFromEmail(email: email)
        } catch is InvalidEmailAdress {
            errorHappenned = true
        } catch {
            XCTAssertTrue(false)
        }

        // Then throw error.
        XCTAssertTrue(errorHappenned)
    }
}
