"use client";

import {
  Card,
  ErrorState,
  LoadingState,
  MetricsCard,
  ResultsTable,
  TrustLevelBadge,
} from "@/components/shared";
import { useBatchAnalysis } from "@/lib/hooks/useAnalysis";
import { useRef, useState } from "react";

export default function CSVBatchPage() {
  const { isLoading, error, result, analyze, progress } = useBatchAnalysis();
  const [columnName, setColumnName] = useState("review_text");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      await analyze(file, columnName);
    } catch (err) {
      console.error("Batch analysis failed:", err);
    }
  };

  const handleExport = () => {
    if (!result) return;

    const csv = [
      ["Index", "Prediction", "Confidence", "Review Text"],
      ...result.results.map(
        (r) =>
          [
            r.index + 1,
            r.prediction === 1 ? "Genuine" : "Fake",
            (r.confidence * 100).toFixed(2) + "%",
            r.review_text,
          ] as (string | number)[],
      ),
    ]
      .map((row) => row.map((cell) => `"${cell}"`).join(","))
      .join("\n");

    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "analysis-results.csv";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2">Batch Analysis</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Upload a CSV file to analyze multiple reviews at once
        </p>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Upload Section */}
        <div className="lg:col-span-2">
          <Card title="Upload CSV File" icon="📁">
            <div className="space-y-4">
              {/* Column Name Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Review Column Name
                </label>
                <input
                  type="text"
                  value={columnName}
                  onChange={(e) => setColumnName(e.target.value)}
                  placeholder="e.g., review_text, review, text"
                  className="w-full px-4 py-2 border dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
                  disabled={isLoading}
                />
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  The name of the CSV column containing review text
                </p>
              </div>

              {/* File Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  CSV File
                </label>
                <div className="relative">
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv"
                    onChange={handleFileSelect}
                    disabled={isLoading}
                    className="hidden"
                  />
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={isLoading}
                    className="w-full px-6 py-8 border-2 border-dashed border-blue-400 dark:border-blue-600 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-center"
                  >
                    <div className="text-3xl mb-2">📤</div>
                    <p className="font-semibold text-gray-900 dark:text-gray-100">
                      Click to upload or drag and drop
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      CSV files only (max 50MB)
                    </p>
                  </button>
                </div>
              </div>

              {/* Format Help */}
              <div className="p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
                <p className="text-sm font-medium text-blue-900 dark:text-blue-100 mb-2">
                  📋 CSV Format
                </p>
                <p className="text-xs text-blue-800 dark:text-blue-300">
                  Your CSV should have a column with review text. Common column
                  names: review_text, review, text, comment, body
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* Info Section */}
        <div className="space-y-4">
          <Card title="Batch Processing" icon="⚙️">
            <div className="space-y-3 text-sm">
              <div>
                <p className="text-gray-600 dark:text-gray-400">
                  Max File Size
                </p>
                <p className="font-semibold">50 MB</p>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-400">
                  Supported Format
                </p>
                <p className="font-semibold">CSV (Comma Separated)</p>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-400">
                  Processing Speed
                </p>
                <p className="font-semibold">~100ms per review</p>
              </div>
            </div>
          </Card>

          <Card title="Results" icon="📊">
            <div className="space-y-2 text-sm">
              {result ? (
                <>
                  <MetricsCard
                    label="Total Reviews"
                    value={result.total_reviews}
                  />
                  <MetricsCard
                    label="Genuine"
                    value={result.genuine_count}
                    variant="success"
                  />
                  <MetricsCard
                    label="Fake"
                    value={result.fake_count}
                    variant="danger"
                  />
                </>
              ) : (
                <p className="text-gray-500 dark:text-gray-400">
                  Upload a file to see results
                </p>
              )}
            </div>
          </Card>
        </div>
      </div>

      {/* Loading State */}
      {isLoading && (
        <LoadingState
          message={`Processing reviews... ${Math.round(progress || 0)}%`}
          progress={progress}
        />
      )}

      {/* Error State */}
      {error && <ErrorState error={error} />}

      {/* Results */}
      {result && !isLoading && (
        <div className="space-y-6">
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
          <Card title="Detailed Results" icon="📋">
            <div className="space-y-4">
              <ResultsTable results={result.results} maxHeight="max-h-96" />
              <button
                onClick={handleExport}
                className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition-colors"
              >
                📥 Export Results as CSV
              </button>
            </div>
          </Card>

          {/* Processing Stats */}
          <Card title="Processing Information" icon="⏱️">
            <div className="grid md:grid-cols-2 gap-4">
              <MetricsCard
                label="Processing Time"
                value={`${result.processing_time.toFixed(2)}s`}
              />
              <MetricsCard
                label="Avg Time per Review"
                value={`${((result.processing_time / result.total_reviews) * 1000).toFixed(0)}ms`}
              />
            </div>
          </Card>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !error && !result && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📁</div>
          <h3 className="text-xl font-semibold mb-2">Ready to Upload</h3>
          <p className="text-gray-600 dark:text-gray-400">
            Select a CSV file above to start batch analysis
          </p>
        </div>
      )}
    </div>
  );
}
