//
//  ContentView.swift
//  MoneyRegrets
//
//  Created by Nathan McGuire on 5/22/25.
//

import SwiftUI
import SwiftData
import Foundation

enum AppSection: String, CaseIterable, Identifiable {
    case dashboard = "Dashboard"
    case accounts = "Accounts"
    case transactions = "Transactions"
    case cashFlow = "Cash Flow"
    case reports = "Reports"
    case budget = "Budget"
    case recurring = "Recurring"
    case goals = "Goals"
    case investments = "Investments"
    case feedback = "Feedback"
    case settings = "Settings"
    case userManagement = "User Management"
    
    var id: String { self.rawValue }
}

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var items: [Item]
    @State private var selectedSection: AppSection? = .dashboard
    @State private var selectedItem: Item?
    
    var body: some View {
        NavigationSplitView(sidebar: {
            VStack(alignment: .leading, spacing: 0) {
                AppBranding()
                    .padding(.bottom, 8)
                Divider()
                List(AppSection.allCases, selection: $selectedSection) { section in
                    NavigationLink(value: section) {
                        Label(section.rawValue, systemImage: icon(for: section))
                    }
                }
            }
#if os(macOS)
            .navigationSplitViewColumnWidth(min: 180, ideal: 220)
#endif
        }, content: {
            switch selectedSection {
            case .dashboard:
                DashboardView()
            case .accounts:
                AccountsView()
            case .transactions:
                TransactionsView(items: items, selectedItem: $selectedItem, addItem: addItem, deleteItems: deleteItems)
            case .cashFlow:
                CashFlowView()
            case .reports:
                ReportsView()
            case .budget:
                BudgetView()
            case .recurring:
                RecurringView()
            case .goals:
                GoalsView()
            case .investments:
                InvestmentsView()
            case .feedback:
                FeedbackView()
            case .settings:
                SettingsView()
            case .userManagement:
                UserManagementView()
            case .none:
                Text("Select a section")
            }
        }, detail: {
            if selectedSection == .transactions, let item = selectedItem {
                VStack(alignment: .leading, spacing: 16) {
                    Text(item.title).font(.title2).bold()
                    Text("Amount: $\(item.amount, specifier: "%.2f")")
                        .font(.headline)
                    Text(item.details)
                        .font(.body)
                    Text("Date: \(item.timestamp, format: Date.FormatStyle(date: .long, time: .shortened))")
                        .font(.caption).foregroundColor(.secondary)
                }
                .padding()
            } else {
                Text("Select an item or section to view details")
                    .foregroundColor(.secondary)
            }
        })
    }

    private func icon(for section: AppSection) -> String {
        switch section {
        case .dashboard: return "rectangle.grid.2x2"
        case .accounts: return "creditcard"
        case .transactions: return "list.bullet.rectangle"
        case .cashFlow: return "arrow.left.arrow.right"
        case .reports: return "chart.bar"
        case .budget: return "dollarsign.circle"
        case .recurring: return "repeat"
        case .goals: return "target"
        case .investments: return "chart.pie"
        case .feedback: return "bubble.left"
        case .settings: return "gear"
        case .userManagement: return "person.2"
        }
    }

    private func addItem() {
        withAnimation {
            let samples = MockFinanceKit.sampleRegrets()
            if let sample = samples.randomElement() {
                let newItem = Item(title: sample.title, amount: sample.amount, details: sample.details, timestamp: sample.timestamp)
                modelContext.insert(newItem)
            }
        }
    }

    private func deleteItems(offsets: IndexSet) {
        withAnimation {
            for index in offsets {
                modelContext.delete(items[index])
            }
        }
    }
}

struct AppBranding: View {
    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: "banknote.fill")
                .resizable()
                .scaledToFit()
                .frame(width: 36, height: 36)
                .foregroundColor(.green)
                .shadow(radius: 2)
            VStack(alignment: .leading, spacing: 2) {
                Text("Money Regrets")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                Text("Finance Insights & Regrets")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 8)
    }
}

// Placeholder views for each section
struct DashboardView: View { var body: some View { Text("Dashboard").font(.largeTitle) } }
struct AccountsView: View { var body: some View { Text("Accounts").font(.largeTitle) } }
struct TransactionsView: View {
    let items: [Item]
    @Binding var selectedItem: Item?
    let addItem: () -> Void
    let deleteItems: (IndexSet) -> Void
    var body: some View {
        List(selection: $selectedItem) {
            ForEach(items) { item in
                NavigationLink(value: item) {
                    VStack(alignment: .leading) {
                        Text(item.title).font(.headline)
                        Text(item.timestamp, format: Date.FormatStyle(date: .numeric, time: .omitted))
                            .font(.caption).foregroundColor(.secondary)
                    }
                }
            }
            .onDelete(perform: deleteItems)
        }
        .toolbar {
            ToolbarItem {
                Button(action: addItem) {
                    Label("Add Regret", systemImage: "plus")
                }
            }
        }
    }
}
struct CashFlowView: View { var body: some View { Text("Cash Flow").font(.largeTitle) } }
struct ReportsView: View { var body: some View { Text("Reports").font(.largeTitle) } }
struct BudgetView: View { var body: some View { Text("Budget").font(.largeTitle) } }
struct RecurringView: View { var body: some View { Text("Recurring").font(.largeTitle) } }
struct GoalsView: View { var body: some View { Text("Goals").font(.largeTitle) } }
struct InvestmentsView: View { var body: some View { Text("Investments").font(.largeTitle) } }
struct FeedbackView: View { var body: some View { Text("Feedback").font(.largeTitle) } }
struct SettingsView: View { var body: some View { Text("Settings").font(.largeTitle) } }
struct UserManagementView: View { var body: some View { Text("User Management").font(.largeTitle) } }

#Preview {
    ContentView()
        .modelContainer(for: Item.self, inMemory: true)
}
