//
//  Item.swift
//  moneyregrets
//
//  Created by Nathan McGuire on 5/22/25.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
