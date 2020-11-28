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
    /// Most common english words. Used to generate description
    let words = ["the","of","and","a","to","in","is","you","that","it","he","was","for","on","are","as","with","his","they","I","at","be","this","have","from","or","one","had","by","word","but","not","what","all","were","we","when","your","can","said","there","use","an","each","which","she","do","how","their","if","will","up","other","about","out","many","then","them","these","so","some","her","would","make","like","him","into","time","has","look","two","more","write","go","see","number","no","way","could","people","my","than","first","water","been","call","who","oil","its","now","find","long","down","day","did","get","come","made","may","part"]
    let defaultUser = User(username: "thisisbillgates", followers: 329, numberOfPosts: 156, profilePicture: UIImage(named: "DefaultProfilePicture")!)
    
    override func setUp() {
        
    }
    
    func testGivenDescriptionIsLessThanMinimumCharacterLongWhenIntializingThenReducedDescriptionSameAsFull() {
        // Given description is less than minimum character long.
        let description = generateDescription(minLength: Post.minimumCharacterReducedDescription - 10, maxLength: Post.minimumCharacterReducedDescription - 1)
        
        // When initializing.
        let descriptionObj = Description(text: description)
        
        // Then reduced description same as full.
        XCTAssertEqual(descriptionObj.fullDescription, descriptionObj.reducedDescription)
    }
    
    func testGivenDescriptionIsMoreThanMinimumCharacterLongWhenIntializingThenReducedDescriptionLessThanFull() {
        // Given description is more than minimum character long.
        let description = generateDescription(minLength: Post.minimumCharacterReducedDescription + 10, maxLength: Post.minimumCharacterReducedDescription + 20)
        
        // When initializing.
        
        let descriptionObj = Description(text: description)
        
        // Then reduced description not same and less than full.
        XCTAssertLessThan(descriptionObj.reducedDescription.count, descriptionObj.fullDescription.count)
    }
    
    func testGivenDescriptionIsMoreThanMinimumCharacterLongWhenIntializingThenReducedDescriptionNotCutInWord() {
        // Given description is more than minimum character long.
        let description = generateDescription(minLength: Post.minimumCharacterReducedDescription + 10, maxLength: Post.minimumCharacterReducedDescription + 20)
        
        // When initializing.
        let descriptionObj = Description(text: description)
        
        // Then reduced description not cut in word.
        XCTAssertEqual(description[descriptionObj.reducedDescription.count - 1], " ")
    }
    /// Methods used to generate descriptions.
    ///
    /// Note that maxLength - minLength must be greater than 6 or infinite loop may occur in rare cases.
    func generateDescription(minLength : Int, maxLength : Int) -> String {
        var description : String = ""
        // The word to add at each iteration
        var word = ""
        while true {
            word = words.randomElement()! + " "
            if (description + word).count > minLength && (description + word).count < maxLength {
                // Both conditions are verified, no need for change, we can send the number.
                return description + word
            } else {
                description += word
            }
        }
    }
}
