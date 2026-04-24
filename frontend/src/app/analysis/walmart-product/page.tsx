"use client";

import {
  Card,
  ErrorState,
  LoadingState,
  MetricsCard,
  ResultsTable,
  TrustLevelBadge,
} from "@/components/shared";
import { useWalmartAnalysis } from "@/lib/hooks/useAnalysis";
import { useState } from "react";

export default function WalmartProductPage() {
  const { isLoading, error, result, analyze, progress } = useWalmartAnalysis();
  const [productId, setProductId] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!productId.trim()) return;

    try {
      await analyze(productId);
    } catch (err) {
      console.error("Walmart analysis failed:", err);
    }
  };

  const handleClear = () => {
    setProductId("");
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2">Walmart Product Analysis</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Scrape and analyze all reviews from a Walmart product
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Input Section */}
        <div className="lg:col-span-2">
          <Card title="Walmart Product ID" icon="🔗">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <input
                  type="text"
                  value={productId}
                  onChange={(e) => setProductId(e.target.value)}
                  placeholder="Enter Product ID or Walmart product number"
                  className="w-full px-4 py-3 border dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
                  disabled={isLoading}
                />
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                  You can find the Product ID in the Walmart URL. For example,
                  in
                  <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">
                    walmart.com/ip/12345678
                  </code>
                  , the Product ID is{" "}
                  <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">
                    12345678
                  </code>
                </p>
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isLoading || !productId.trim()}
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-400 text-white font-semibold rounded-lg hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  {isLoading ? "Scraping & Analyzing..." : "Analyze Product"}
                </button>
                <button
                  type="button"
                  onClick={handleClear}
                  disabled={isLoading}
                  className="px-6 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 font-semibold rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Clear
                </button>
              </div>
            </form>
          </Card>
        </div>

        {/* Info Section */}
        <div className="space-y-4">
          <Card title="How to Find Product ID" icon="🔎">
            <div className="space-y-3 text-sm">
              <div>
                <p className="font-semibold text-gray-700 dark:text-gray-300">
                  Option 1: From URL
                </p>
                <p className="text-gray-600 dark:text-gray-400">
                  Look for{" "}
                  <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded text-xs">
                    /ip/
                  </code>{" "}
                  in the URL
                </p>
              </div>
              <div>
                <p className="font-semibold text-gray-700 dark:text-gray-300">
                  Option 2: Product Page
                </p>
                <p className="text-gray-600 dark:text-gray-400">
                  Check the product page source or network tab
                </p>
              </div>
              <div>
                <p className="font-semibold text-gray-700 dark:text-gray-300">
                  Example
                </p>
                <p className="text-gray-600 dark:text-gray-400 font-mono text-xs">
                  Product ID: 12345678
                </p>
              </div>
            </div>
          </Card>

          <Card title="Features" icon="✨">
            <ul className="text-sm space-y-2 text-gray-600 dark:text-gray-400">
              <li>✅ Full review scraping</li>
              <li>✅ Real-time analysis</li>
              <li>✅ Ratings & helpfulness</li>
              <li>✅ Trust score calculation</li>
              <li>✅ Exportable results</li>
            </ul>
          </Card>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <LoadingState
          message={`Scraping and analyzing reviews... ${Math.round(progress || 0)}%`}
          progress={progress}
        />
      )}

      {/* Error State */}
      {error && <ErrorState error={error} />}

      {/* Results */}
      {result && !isLoading && (
        <div className="space-y-6">
          {/* Product Info */}
          {result.product_info && (
            <Card title="Product Information" icon="📦">
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Product Name
                  </p>
                  <p className="text-lg font-semibold">
                    {result.product_info.title || "N/A"}
                  </p>
                </div>
                {result.product_info.rating && (
                  <div className="flex gap-4">
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Rating
                      </p>
                      <p className="text-lg font-semibold">
                        ⭐ {result.product_info.rating.toFixed(1)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Review Count
                      </p>
                      <p className="text-lg font-semibold">
                        {result.product_info.review_count}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </Card>
          )}

          {/* Summary */}
          <div className="grid md:grid-cols-4 gap-4">
            <MetricsCard
              label="Total Reviews"
              value={result.total_reviews}
              icon="📈"
            />
            <MetricsCard
              label="Genuine"
              value={`${result.genuine_count} (${result.genuine_percentage.toFixed(1)}%)`}
              icon="✅"
              variant="success"
            />
            <MetricsCard
              label="Fake"
              value={`${result.fake_count} (${result.fake_percentage.toFixed(1)}%)`}
              icon="❌"
              variant="danger"
            />
            <Card title="Trust Level" icon="⭐">
              <TrustLevelBadge
                trustLevel={result.trust_level}
                showLabel={true}
              />
            </Card>
          </div>

          {/* Results Table */}
          <Card title="Review Analysis" icon="📋">
            <ResultsTable results={result.results} maxHeight="max-h-96" />
          </Card>

          {/* Processing Stats */}
          <Card title="Processing Information" icon="⏱️">
            <div className="grid md:grid-cols-3 gap-4">
              <MetricsCard
                label="Scraping Time"
                value={`${result.scraping_time.toFixed(2)}s`}
              />
              <MetricsCard
                label="Analysis Time"
                value={`${result.processing_time.toFixed(2)}s`}
              />
              <MetricsCard
                label="Total Time"
                value={`${(result.scraping_time + result.processing_time).toFixed(2)}s`}
              />
            </div>
          </Card>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !error && !result && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🏪</div>
          <h3 className="text-xl font-semibold mb-2">Ready to Analyze</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Enter a Walmart Product ID above to get started
          </p>
        </div>
      )}
    </div>
  );
}
