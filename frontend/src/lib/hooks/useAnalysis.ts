'use client';

/**
 * Custom hooks for analysis functionality
 */

import { useCallback, useState } from 'react';
import * as api from '../api';
import { BatchAnalysisResponse, ProductScrapingResponse, SingleReviewResponse } from '../types';

/**
 * Hook for managing single review analysis
 */
export function useSingleReviewAnalysis() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const [result, setResult] = useState<SingleReviewResponse | undefined>();

  const analyze = useCallback(
    async (reviewText: string, useEnsemble = true) => {
      setIsLoading(true);
      setError(undefined);
      try {
        const res = await api.analyzeReview({
          review_text: reviewText,
          use_ensemble: useEnsemble,
        });
        setResult(res);
        setIsLoading(false);
        return res;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Analysis failed';
        setError(errorMessage);
        setIsLoading(false);
        throw err;
      }
    },
    []
  );

  const reset = useCallback(() => {
    setIsLoading(false);
    setError(undefined);
    setResult(undefined);
  }, []);

  return { isLoading, error, result, analyze, reset };
}

/**
 * Hook for managing batch analysis
 */
export function useBatchAnalysis() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const [result, setResult] = useState<BatchAnalysisResponse | undefined>();
  const [progress, setProgress] = useState(0);

  const analyze = useCallback(
    async (file: File, columnName: string) => {
      setIsLoading(true);
      setError(undefined);
      setProgress(20);
      try {
        setProgress(40);
        const res = await api.analyzeBatch(file, columnName);
        setResult(res);
        setProgress(100);
        setIsLoading(false);
        return res;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Batch analysis failed';
        setError(errorMessage);
        setProgress(0);
        setIsLoading(false);
        throw err;
      }
    },
    []
  );

  const reset = useCallback(() => {
    setIsLoading(false);
    setError(undefined);
    setResult(undefined);
    setProgress(0);
  }, []);

  return { isLoading, error, result, progress, analyze, reset };
}

/**
 * Hook for managing Amazon product analysis
 */
export function useAmazonAnalysis() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const [result, setResult] = useState<ProductScrapingResponse | undefined>();
  const [progress, setProgress] = useState(0);

  const analyze = useCallback(
    async (productUrl: string) => {
      setIsLoading(true);
      setError(undefined);
      setProgress(20);
      try {
        setProgress(50);
        const res = await api.analyzeAmazonProduct({
          product_url: productUrl,
          include_analysis: true,
        });
        setResult(res);
        setProgress(100);
        setIsLoading(false);
        return res;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Amazon analysis failed';
        setError(errorMessage);
        setProgress(0);
        setIsLoading(false);
        throw err;
      }
    },
    []
  );

  const reset = useCallback(() => {
    setIsLoading(false);
    setError(undefined);
    setResult(undefined);
    setProgress(0);
  }, []);

  return { isLoading, error, result, progress, analyze, reset };
}

/**
 * Hook for managing Walmart product analysis
 */
export function useWalmartAnalysis() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();
  const [result, setResult] = useState<ProductScrapingResponse | undefined>();
  const [progress, setProgress] = useState(0);

  const analyze = useCallback(
    async (productId: string) => {
      setIsLoading(true);
      setError(undefined);
      setProgress(20);
      try {
        setProgress(50);
        const res = await api.analyzeWalmartProduct({
          product_id: productId,
          include_analysis: true,
        });
        setResult(res);
        setProgress(100);
        setIsLoading(false);
        return res;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Walmart analysis failed';
        setError(errorMessage);
        setProgress(0);
        setIsLoading(false);
        throw err;
      }
    },
    []
  );

  const reset = useCallback(() => {
    setIsLoading(false);
    setError(undefined);
    setResult(undefined);
    setProgress(0);
  }, []);

  return { isLoading, error, result, progress, analyze, reset };
}
