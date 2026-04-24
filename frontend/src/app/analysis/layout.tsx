"use client";

import { ThemeToggle } from "@/components/shared";
import Link from "next/link";
import { useState } from "react";

/**
 * Layout for all analysis pages
 * Provides navigation and consistent structure
 */
export default function AnalysisLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [activeTab, setActiveTab] = useState<string>("single-review");

  const tabs = [
    {
      id: "single-review",
      label: "📝 Single Review",
      href: "/analysis/single-review",
    },
    { id: "csv-batch", label: "📊 CSV Batch", href: "/analysis/csv-batch" },
    {
      id: "amazon-product",
      label: "🛍️ Amazon",
      href: "/analysis/amazon-product",
    },
    {
      id: "walmart-product",
      label: "🏪 Walmart",
      href: "/analysis/walmart-product",
    },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-white dark:bg-gray-900">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link
              href="/"
              className="flex items-center gap-2 text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent hover:opacity-80 transition-opacity"
            >
              🔍 FakeReview.AI
            </Link>
            <ThemeToggle />
          </div>

          {/* Tab Navigation */}
          <div className="flex gap-2 overflow-x-auto pb-3 -mb-px">
            {tabs.map((tab) => (
              <Link
                key={tab.id}
                href={tab.href}
                className={`px-4 py-2 whitespace-nowrap rounded-t-lg font-medium transition-colors border-b-2 ${
                  activeTab === tab.id
                    ? "border-blue-600 text-blue-600 dark:text-blue-400 dark:border-blue-400"
                    : "border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-300"
                }`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-4 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-gray-600 dark:text-gray-400">
          <p>© 2026 Fake Review Detection. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
