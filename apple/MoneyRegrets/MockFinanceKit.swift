//  MockFinanceKit.swift
//  MoneyRegrets
//
//  Simulates FinanceKit for development without a developer account.

import Foundation

struct MockRegret {
    let title: String
    let amount: Double
    let details: String
    let timestamp: Date
}

struct MockFinanceKit {
    static func sampleRegrets() -> [MockRegret] {
        return [
            MockRegret(title: "Impulse Buy: Expensive Coffee", amount: 6.50, details: "Bought a fancy coffee drink I didn't need.", timestamp: Date().addingTimeInterval(-86400)),
            MockRegret(title: "Unused Gym Membership", amount: 120.00, details: "Signed up for a gym and never went.", timestamp: Date().addingTimeInterval(-604800)),
            MockRegret(title: "Gadget FOMO", amount: 299.99, details: "Bought a gadget on launch day, barely used it.", timestamp: Date().addingTimeInterval(-2592000)),
            MockRegret(title: "Streaming Subscriptions", amount: 45.00, details: "Forgot to cancel unused streaming services.", timestamp: Date().addingTimeInterval(-172800)),
        ]
    }
}
