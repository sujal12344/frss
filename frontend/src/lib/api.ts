/**
 * API service layer for backend communication
 * Handles all HTTP requests to the Streamlit backend
 */

import {
    AmazonProductRequest,
    BatchAnalysisResponse,
    ProductScrapingResponse,
    SingleReviewRequest,
    SingleReviewResponse,
    WalmartProductRequest
} from './types';

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8501';
const API_TIMEOUT = 60000; // 60 seconds
const MAX_RETRIES = 3;

/**
 * Enhanced fetch with retry logic and error handling
 */
async function fetchWithRetry(
  url: string,
  options: RequestInit = {},
  retries = MAX_RETRIES
): Promise<Response> {
  let lastError: Error | null = null;

  for (let i = 0; i < retries; i++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new APIError(
          response.status,
          `API returned status ${response.status}`
        );
      }

      return response;
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      // Don't retry on client errors (4xx) or if it's the last attempt
      if (error instanceof APIError && error.status < 500) {
        throw error;
      }

      if (i < retries - 1) {
        // Exponential backoff: 1s, 2s, 4s
        await new Promise((resolve) => setTimeout(resolve, Math.pow(2, i) * 1000));
      }
    }
  }

  throw lastError || new Error('Failed after retries');
}

/**
 * Helper to throw structured API errors
 */
class APIError extends Error {
  constructor(
    public status: number,
    message: string,
    public details?: unknown
  ) {
    super(message);
    this.name = 'APIError';
  }
}

/**
 * Analyze a single review
 */
export async function analyzeReview(
  request: SingleReviewRequest
): Promise<SingleReviewResponse> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/api/analyze-review`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    const data = await response.json();
    return data as SingleReviewResponse;
  } catch (error) {
    throw handleAPIError(error);
  }
}

/**
 * Analyze batch of reviews from CSV
 */
export async function analyzeBatch(file: File, columnName: string): Promise<BatchAnalysisResponse> {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('column_name', columnName);

    const response = await fetchWithRetry(`${API_BASE_URL}/api/analyze-batch`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    return data as BatchAnalysisResponse;
  } catch (error) {
    throw handleAPIError(error);
  }
}

/**
 * Scrape and analyze Amazon product reviews
 */
export async function analyzeAmazonProduct(
  request: AmazonProductRequest
): Promise<ProductScrapingResponse> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/api/analyze-amazon-product`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    const data = await response.json();
    return data as ProductScrapingResponse;
  } catch (error) {
    throw handleAPIError(error);
  }
}

/**
 * Scrape and analyze Walmart product reviews
 */
export async function analyzeWalmartProduct(
  request: WalmartProductRequest
): Promise<ProductScrapingResponse> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/api/analyze-walmart-product`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    const data = await response.json();
    return data as ProductScrapingResponse;
  } catch (error) {
    throw handleAPIError(error);
  }
}

/**
 * Get available models and metrics
 */
export async function getModelsInfo(): Promise<{
  models: string[];
  metrics: Record<string, unknown>;
}> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/api/models-info`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    return data;
  } catch (error) {
    throw handleAPIError(error);
  }
}

/**
 * Get trust levels configuration
 */
export async function getTrustLevels(): Promise<Record<string, unknown>> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/api/trust-levels`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();
    return data;
  } catch (error) {
    throw handleAPIError(error);
  }
}

/**
 * Health check for backend
 */
export async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetchWithRetry(`${API_BASE_URL}/api/health`, {
      method: 'GET',
    });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Handle and normalize API errors
 */
function handleAPIError(error: unknown): APIError {
  if (error instanceof APIError) {
    return error;
  }

  if (error instanceof Error) {
    if (error.message === 'Failed to fetch') {
      return new APIError(0, 'Network error - unable to connect to backend');
    }
    return new APIError(500, error.message);
  }

  return new APIError(500, 'An unexpected error occurred');
}

/**
 * Export for convenience
 */
export { APIError };

