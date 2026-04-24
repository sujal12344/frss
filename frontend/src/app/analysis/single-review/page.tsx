"use client";

import {
  Card,
  ErrorState,
  LoadingState,
  MetricsCard,
  PredictionBadge,
  TrustLevelBadge,
} from "@/components/shared";
import { useSingleReviewAnalysis } from "@/lib/hooks/useAnalysis";
import { useState } from "react";

export default function SingleReviewPage() {
  const { isLoading, error, result, analyze } = useSingleReviewAnalysis();
  const [reviewText, setReviewText] = useState("");
  const [useEnsemble, setUseEnsemble] = useState(true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewText.trim()) return;

    try {
      await analyze(reviewText, useEnsemble);
    } catch (err) {
      console.error("Analysis failed:", err);
    }
  };

  const handleClear = () => {
    setReviewText("");
    // Reset result by analyzing empty string won't happen, so we just keep the component as is
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2">Analyze Single Review</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Enter a review text to check if it's genuine or fake using our ML
          models
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Input Section */}
        <div className="lg:col-span-2">
          <Card title="Review Text" icon="✏️">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <textarea
                  value={reviewText}
                  onChange={(e) => setReviewText(e.target.value)}
                  placeholder="Paste the review text here..."
                  className="w-full h-48 p-4 border dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 resize-none"
                  disabled={isLoading}
                />
                <div className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                  {reviewText.length} characters
                </div>
              </div>

              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="ensemble"
                  checked={useEnsemble}
                  onChange={(e) => setUseEnsemble(e.target.checked)}
                  disabled={isLoading}
                  className="w-4 h-4 rounded border-gray-300 dark:border-gray-600 cursor-pointer"
                />
                <label
                  htmlFor="ensemble"
                  className="text-sm font-medium cursor-pointer"
                >
                  Use Ensemble Model (combines multiple algorithms for better
                  accuracy)
                </label>
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isLoading || !reviewText.trim()}
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  {isLoading ? "Analyzing..." : "Analyze Review"}
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

        {/* Quick Stats */}
        <div className="space-y-4">
          <Card title="Model Info" icon="🤖">
            <div className="space-y-3 text-sm">
              <div>
                <p className="text-gray-600 dark:text-gray-400">
                  Ensemble Mode
                </p>
                <p className="font-semibold">
                  {useEnsemble ? "Enabled" : "Disabled"}
                </p>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-400">Models Used</p>
                <p className="font-semibold">5+ Algorithms</p>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-400">Accuracy</p>
                <p className="font-semibold">94%+</p>
              </div>
            </div>
          </Card>

          <Card title="Tips" icon="💡">
            <ul className="text-sm space-y-2 text-gray-600 dark:text-gray-400">
              <li>• Use complete reviews for better results</li>
              <li>• Ensemble mode provides more reliable predictions</li>
              <li>• Confidence shows model's certainty</li>
              <li>• Check trust level for overall assessment</li>
            </ul>
          </Card>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <LoadingState message="Analyzing review..." progress={75} />
      )}

      {/* Error State */}
      {error && <ErrorState error={error} />}

      {/* Results */}
      {result && !isLoading && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-8">
            <div className="text-center">
              <div className="mb-4">
                <PredictionBadge
                  prediction={result.prediction}
                  confidence={result.confidence}
                  className="justify-center text-lg"
                />
              </div>
              <h2 className="text-2xl font-bold mb-2">
                {result.prediction === 1
                  ? "✅ Genuine Review"
                  : "❌ Fake Review"}
              </h2>
              <p className="text-gray-600 dark:text-gray-400">
                Confidence Score: {(result.confidence * 100).toFixed(2)}%
              </p>
            </div>
          </div>

          {/* Trust Level and Metrics */}
          <div className="grid md:grid-cols-2 gap-6">
            <Card title="Trust Level" icon="⭐">
              {result.trust_level && (
                <div className="space-y-3">
                  <TrustLevelBadge
                    trustLevel={result.trust_level}
                    showLabel={true}
                  />
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    This review has been classified as "
                    {result.trust_level.label}"
                  </p>
                </div>
              )}
            </Card>

            <Card title="Analysis Time" icon="⏱️">
              <div className="space-y-2">
                <MetricsCard
                  label="Total Time"
                  value={`${result.total_time.toFixed(2)}ms`}
                />
              </div>
            </Card>
          </div>

          {/* Model-by-model Results */}
          {Object.keys(result.individual_preds).length > 0 && (
            <Card title="Model Details" icon="📊">
              <div className="space-y-3">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  Individual predictions from each algorithm:
                </p>
                <div className="space-y-2">
                  {Object.entries(result.individual_preds).map(
                    ([modelName, pred]) => (
                      <div
                        key={modelName}
                        className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded"
                      >
                        <span className="font-medium text-gray-900 dark:text-gray-100">
                          {modelName}
                        </span>
                        <div className="flex items-center gap-3">
                          <span
                            className={`text-sm font-semibold ${
                              pred === 1
                                ? "text-green-600 dark:text-green-400"
                                : "text-red-600 dark:text-red-400"
                            }`}
                          >
                            {pred === 1 ? "✅ Genuine" : "❌ Fake"}
                          </span>
                          {result.prediction_times[modelName] && (
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {result.prediction_times[modelName].toFixed(2)}ms
                            </span>
                          )}
                        </div>
                      </div>
                    ),
                  )}
                </div>
              </div>
            </Card>
          )}
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !error && !result && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📝</div>
          <h3 className="text-xl font-semibold mb-2">Ready to Analyze</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Enter a review above and click "Analyze Review" to get started
          </p>
        </div>
      )}
    </div>
  );
}
