//
//  CacheStorage.swift
//  Bestagram
//
//  Created by Titouan Blossier on 25/01/2021.
//

import Foundation
import Cache

class CacheStorage {
    static let shared = CacheStorage()
    private init() { }

    static let memoryConfig = MemoryConfig(expiry: .never, countLimit: 100, totalCostLimit: 100000)
    // 100 objects max with 100mb of memory used max.
    static let diskConfig = DiskConfig(name: "Storage", expiry: .never, maxSize: 1000000000, protectionType: .complete)
    // Max size of 1gb
    let storage = try! Storage<String, String>(diskConfig: diskConfig, memoryConfig: memoryConfig, transformer: TransformerFactory.forCodable(ofType: String.self))
}
