"use client";

/**
 * Reusable UI Components
 */

import { useTheme } from "@/lib/context/ThemeContext";
import {
  BatchReviewResult,
  ErrorStateProps,
  LoadingStateProps,
  TrustLevel,
} from "@/lib/types";
import React from "react";

// ==================== Trust Level Badge ====================

interface TrustLevelBadgeProps {
  trustLevel?: TrustLevel;
  showLabel?: boolean;
  className?: string;
}

export function TrustLevelBadge({
  trustLevel,
  showLabel = true,
  className = "",
}: TrustLevelBadgeProps) {
  if (!trustLevel) return null;
  const getTrustColor = (label: string) => {
    if (label.includes("Genuine") || label.includes("Authentic"))
      return "bg-green-500";
    if (label.includes("Fake") || label.includes("Dominated"))
      return "bg-red-500";
    if (label.includes("Balanced") || label.includes("Mixed"))
      return "bg-yellow-500";
    return "bg-blue-500";
  };

  return (
    <div className={`inline-flex items-center gap-2 ${className}`}>
      <div
        className={`w-3 h-3 rounded-full ${getTrustColor(trustLevel.label)}`}
      />
      {showLabel && (
        <span className="text-sm font-medium">{trustLevel.label}</span>
      )}
    </div>
  );
}

// ==================== Prediction Badge ====================

interface PredictionBadgeProps {
  prediction: 0 | 1;
  confidence: number;
  className?: string;
}

export function PredictionBadge({
  prediction,
  confidence,
  className = "",
}: PredictionBadgeProps) {
  const isGenuine = prediction === 1;
  const bgColor = isGenuine
    ? "bg-green-100 dark:bg-green-900"
    : "bg-red-100 dark:bg-red-900";
  const textColor = isGenuine
    ? "text-green-800 dark:text-green-200"
    : "text-red-800 dark:text-red-200";
  const borderColor = isGenuine
    ? "border-green-300 dark:border-green-700"
    : "border-red-300 dark:border-red-700";
  const label = isGenuine ? "✅ Genuine" : "❌ Fake";

  return (
    <div
      className={`px-3 py-1 rounded-full border ${bgColor} ${textColor} ${borderColor} text-sm font-medium ${className}`}
    >
      {label} ({(confidence * 100).toFixed(1)}%)
    </div>
  );
}

// ==================== Loading State ====================

export function LoadingState({
  message = "Analyzing...",
  progress,
}: LoadingStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-4">
      <div className="inline-block">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
      </div>
      <p className="text-lg font-medium text-gray-700 dark:text-gray-300">
        {message}
      </p>
      {progress !== undefined && (
        <div className="w-full max-w-md bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            className="bg-blue-500 h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}

// ==================== Error State ====================

export function ErrorState({ error, onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
      <div className="text-4xl">⚠️</div>
      <div className="text-center">
        <h3 className="text-lg font-semibold text-red-800 dark:text-red-200 mb-2">
          Error
        </h3>
        <p className="text-sm text-red-600 dark:text-red-300">{error}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-medium transition-colors"
        >
          Retry
        </button>
      )}
    </div>
  );
}

// ==================== Metrics Card ====================

interface MetricsCardProps {
  label: string;
  value: string | number;
  icon?: string;
  variant?: "default" | "success" | "danger" | "warning";
  className?: string;
}

export function MetricsCard({
  label,
  value,
  icon,
  variant = "default",
  className = "",
}: MetricsCardProps) {
  const bgColors = {
    default:
      "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800",
    success:
      "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800",
    danger: "bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800",
    warning:
      "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800",
  };

  const textColors = {
    default: "text-blue-900 dark:text-blue-100",
    success: "text-green-900 dark:text-green-100",
    danger: "text-red-900 dark:text-red-100",
    warning: "text-yellow-900 dark:text-yellow-100",
  };

  return (
    <div className={`p-4 border rounded-lg ${bgColors[variant]} ${className}`}>
      <div className="flex items-center gap-3">
        {icon && <span className="text-2xl">{icon}</span>}
        <div>
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
            {label}
          </p>
          <p className={`text-2xl font-bold ${textColors[variant]}`}>{value}</p>
        </div>
      </div>
    </div>
  );
}

// ==================== Results Table ====================

interface ResultsTableProps {
  results: BatchReviewResult[];
  onFilter?: (prediction?: 0 | 1) => void;
  isLoading?: boolean;
  maxHeight?: string;
}

export function ResultsTable({
  results,
  onFilter,
  isLoading = false,
  maxHeight = "max-h-96",
}: ResultsTableProps) {
  const [filterPrediction, setFilterPrediction] = React.useState<
    0 | 1 | undefined
  >(undefined);

  const filteredResults = filterPrediction
    ? results.filter((r) => r.prediction === filterPrediction)
    : results;

  const handleFilter = (pred: 0 | 1 | undefined) => {
    setFilterPrediction(pred);
    onFilter?.(pred);
  };

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <button
          onClick={() => handleFilter(undefined)}
          className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
            filterPrediction === undefined
              ? "bg-blue-500 text-white"
              : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
          }`}
        >
          All ({results.length})
        </button>
        <button
          onClick={() => handleFilter(1)}
          className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
            filterPrediction === 1
              ? "bg-green-500 text-white"
              : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
          }`}
        >
          Genuine ({results.filter((r) => r.prediction === 1).length})
        </button>
        <button
          onClick={() => handleFilter(0)}
          className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
            filterPrediction === 0
              ? "bg-red-500 text-white"
              : "bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200"
          }`}
        >
          Fake ({results.filter((r) => r.prediction === 0).length})
        </button>
      </div>

      <div
        className={`overflow-y-auto ${maxHeight} border dark:border-gray-700 rounded-lg`}
      >
        {filteredResults.length === 0 ? (
          <div className="p-4 text-center text-gray-500 dark:text-gray-400">
            No results found
          </div>
        ) : (
          <table className="w-full text-sm">
            <thead className="sticky top-0 bg-gray-50 dark:bg-gray-900 border-b dark:border-gray-700">
              <tr>
                <th className="px-4 py-2 text-left font-semibold text-gray-700 dark:text-gray-300">
                  Index
                </th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700 dark:text-gray-300">
                  Prediction
                </th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700 dark:text-gray-300">
                  Confidence
                </th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700 dark:text-gray-300">
                  Review Text
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredResults.map((result, idx) => (
                <tr
                  key={result.index}
                  className="border-t dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  <td className="px-4 py-2 font-medium text-gray-900 dark:text-gray-100">
                    {result.index + 1}
                  </td>
                  <td className="px-4 py-2">
                    <PredictionBadge
                      prediction={result.prediction}
                      confidence={result.confidence}
                    />
                  </td>
                  <td className="px-4 py-2 text-gray-700 dark:text-gray-300">
                    {(result.confidence * 100).toFixed(1)}%
                  </td>
                  <td
                    className="px-4 py-2 text-gray-600 dark:text-gray-400 truncate max-w-xs"
                    title={result.review_text}
                  >
                    {result.review_text.substring(0, 50)}...
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

// ==================== Card Component ====================

interface CardProps {
  title: string;
  children: React.ReactNode;
  icon?: string;
  className?: string;
}

export function Card({ title, children, icon, className = "" }: CardProps) {
  return (
    <div
      className={`p-6 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-lg shadow-sm ${className}`}
    >
      <div className="flex items-center gap-2 mb-4">
        {icon && <span className="text-2xl">{icon}</span>}
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          {title}
        </h3>
      </div>
      {children}
    </div>
  );
}

// ==================== Theme Toggle ====================

export function ThemeToggle() {
  const { isDarkMode, toggleDarkMode } = useTheme();

  return (
    <button
      onClick={toggleDarkMode}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
      aria-label="Toggle theme"
    >
      {isDarkMode ? "☀️" : "🌙"}
    </button>
  );
}
