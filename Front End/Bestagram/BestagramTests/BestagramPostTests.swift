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
    override func setUp() {
        super.setUp()
    }

    // MARK: - Description tests

    /// Most common english words. Used to generate description
    let words = [
        "the", "of", "and", "a", "to", "in", "is", "you", "that", "it", "he", "was", "for",
        "on", "are", "as", "with", "his", "they", "I", "at", "be", "this", "have", "from",
        "or", "one", "had", "by", "word", "but", "not", "what", "all", "were", "we", "when",
        "your", "can", "said", "there", "use", "an", "each", "which", "she", "do", "how",
        "their", "if", "will", "up", "other", "about", "out", "many", "then", "them", "these",
        "so", "some", "her", "would", "make", "like", "him", "into", "time", "has", "look",
        "two", "more", "write", "go", "see", "number", "no", "way", "could", "people", "my",
        "than", "first", "water", "been", "call", "who", "oil", "its", "now", "find", "long",
        "down", "day", "did", "get", "come", "made", "may", "part"
    ]

    let defaultUser = User(
        username: "thisisbillgates",
        followers: 329,
        numberOfPosts: 156,
        // swiftlint:disable:next force_unwrapping
        profilePicture: UIImage(named: "DefaultProfilePicture")!)

    func testGivenDescriptionIsLessThanMinimumCharacterLongWhenIntializingThenReducedDescriptionSameAsFull() {
        // Given description is less than minimum character long.
        let description = generateDescription(
            minLength: Post.minimumCharacterReducedDescription - 10,
            maxLength: Post.minimumCharacterReducedDescription - 1
        )

        // When initializing.
        let descriptionObj = Description(text: description)

        // Then reduced description same as full.
        XCTAssertEqual(descriptionObj.fullDescription, descriptionObj.reducedDescription)
    }

    func testGivenDescriptionIsMoreThanMinimumCharacterLongWhenIntializingThenReducedDescriptionLessThanFull() {
        // Given description is more than minimum character long.
        let description = generateDescription(
            minLength: Post.minimumCharacterReducedDescription + 10,
            maxLength: Post.minimumCharacterReducedDescription + 20
        )

        // When initializing.

        let descriptionObj = Description(text: description)

        // Then reduced description not same and less than full.
        XCTAssertLessThan(descriptionObj.reducedDescription.count, descriptionObj.fullDescription.count)
    }

    func testGivenDescriptionIsMoreThanMinimumCharacterLongWhenIntializingThenReducedDescriptionNotCutInWord() {
        // Given description is more than minimum character long.
        let description = generateDescription(
            minLength: Post.minimumCharacterReducedDescription + 10,
            maxLength: Post.minimumCharacterReducedDescription + 20)

        // When initializing.
        let descriptionObj = Description(text: description)

        // Then reduced description not cut in word.
        XCTAssertEqual(description[descriptionObj.reducedDescription.count], " ")
    }
    /// Methods used to generate descriptions.
    ///
    /// Note that maxLength - minLength must be greater than 6 or infinite loop may occur in rare cases.
    func generateDescription(minLength: Int, maxLength: Int) -> String {
        var description: String = ""
        // The word to add at each iteration
        var word = ""
        while true {
            // Word is a hand crafted array and never modified so a random element can't be nil.
            // switlint:disable:next force_unwrapping
            word = words.randomElement()! + " "
            if (description + word).count > minLength && (description + word).count < maxLength {
                // Both conditions are verified, no need for change, we can send the number.
                return description + word
            } else {
                description += word
            }
        }
    }

    // MARK: - Time tests
    func testGivenPostWasMade37SecondsAgoWhenGettingDisplayedDateInformationThenIs37SecondsAgo() {
        // Given post was made 37 seconds ago.
        let date = Date(timeIntervalSinceNow: TimeInterval(-37))
        let post = makePost(postTime: date)

        // When getting displayed date information.
        let displayedDateInformation: String = post.getDisplayPostDateInformation()

        // Then is 37 seconds ago.
        XCTAssertEqual(displayedDateInformation, "37 seconds ago")
    }

    func testGivenPostWasMade5Point9MinutesAgoWhenGettingDisplayedDateThenIs5MinutesAgo() {
        // Given post was made 5.9 minutes ago.
        let date = Date(timeIntervalSinceNow: -TimeInterval(5.9 * 60))
        let post = makePost(postTime: date)

        // When getting displayed date.
        let displayedDateInformation: String = post.getDisplayPostDateInformation()

        // Then is 5 minutes ago.
        XCTAssertEqual(displayedDateInformation, "5 minutes ago")
    }

    func testGivenPostWasMade1Point9SecondAgoWhenGettingDisplayedDateThenIs1SecondAgo() {
        // Given post was made 1.9 second ago.
        let date = Date(timeIntervalSinceNow: -TimeInterval(1.9))
        let post = makePost(postTime: date)

        // When getting displayed date.
        let displayedDateInformation: String = post.getDisplayPostDateInformation()

        // Then is 5 minutes ago.
        XCTAssertEqual(displayedDateInformation, "1 second ago")
    }

    func makePost(
        user: User? = nil,
        image: UIImage = UIImage(),
        numberOfLikes: Int = 327,
        description: String = "default description used for testing",
        postTime: Date = Date(timeIntervalSinceNow: TimeInterval(-7654))) -> Post {
        /// Function created to facilitate the creation of post in unit testing.
        ///
        /// All the fields are filled by default so the developper can focus on modifying what's important.

        // User can't be automatically filled with default user so we fill it here (Cannot use
        // instance member 'defaultUser' as a default parameter)
        if let givenUser = user {
            return Post(
                user: givenUser,
                image: image,
                numberOfLikes: numberOfLikes,
                description: description,
                postTime: postTime
            )
        } else {
            return Post(
                user: defaultUser,
                image: image,
                numberOfLikes: numberOfLikes,
                description: description,
                postTime: postTime
            )
        }
    }
}
