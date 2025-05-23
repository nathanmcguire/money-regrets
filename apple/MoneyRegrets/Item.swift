//
//  Item.swift
//  MoneyRegrets
//
//  Created by Nathan McGuire on 5/22/25.
//

import Foundation
import SwiftData

@Model
final class Item {
    var title: String
    var amount: Double
    var details: String // Renamed from description to details
    var timestamp: Date
    
    init(title: String, amount: Double, details: String, timestamp: Date) {
        self.title = title
        self.amount = amount
        self.details = details
        self.timestamp = timestamp
    }
}
