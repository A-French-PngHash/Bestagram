//
//  BestagramPostTest.swift
//  BestagramTests
//
//  Created by Titouan Blossier on 28/11/2020.
//

import XCTest
@testable import Bestagram

/// Tests the different methods in the Post class
class BestagramPostTests: XCTestCase {
    let letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    let defaultUser = User(username: "thisisbillgates", followers: 329, numberOfPosts: 156, profilePicture: UIImage(named: "DefaultProfilePicture")!)
    
    override func setUp() {
        
    }
    
    func testGivenDescriptionIsLessThanMinimumCharacterLongWhenIntializingThenReducedDescriptionSameAsFull() {
        // Given description is less than thirty character long.
        let description = randomString(length: Post.minimumCharacterReducedDescription - 2)
        
        // When initializing.
        let post = Post(user: defaultUser, image: UIImage(), numberOfLikes: 132, description: description)
        
        // Then reduced description same as full.
        XCTAssertEqual(post.fullDescription, post.reducedDescription)
    }
    
    
    func randomString(length: Int) -> String {
      return String((0..<length).map{ _ in letters.randomElement()! })
    }
}
