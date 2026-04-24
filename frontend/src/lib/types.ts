/**
 * Shared TypeScript types and interfaces
 */

// ==================== API Response Types ====================

export interface PredictionResult {
  prediction: 0 | 1; // 0 = Fake, 1 = Genuine
  confidence: number; // 0-1
  individual_preds: Record<string, number>;
  prediction_times: Record<string, number>;
  total_time: number;
  trust_level?: TrustLevel;
}

export interface TrustLevel {
  threshold: number;
  label: string;
}

export interface AnalysisMetrics {
  total_reviews: number;
  genuine_count: number;
  fake_count: number;
  genuine_percentage: number;
  fake_percentage: number;
  trust_level: TrustLevel;
}

export interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  sensitivity?: number;
}

export interface ModelInfo {
  name: string;
  metrics?: ModelMetrics;
  prediction_time?: number;
  confidence?: number;
}

// ==================== Single Review Types ====================

export interface SingleReviewRequest {
  review_text: string;
  use_ensemble?: boolean;
}

export interface SingleReviewResponse extends PredictionResult {
  review_text: string;
}

// ==================== Batch Analysis Types ====================

export interface BatchReviewResult {
  index: number;
  review_text: string;
  prediction: 0 | 1;
  confidence: number;
}

export interface BatchAnalysisResponse extends AnalysisMetrics {
  results: BatchReviewResult[];
  processing_time: number;
}

// ==================== Product Scraping Types ====================

export interface ProductReview {
  id?: string;
  author?: string;
  rating?: number;
  date?: string;
  title?: string;
  text: string;
  helpful_count?: number;
}

export interface AmazonProductRequest {
  product_url: string;
  include_analysis?: boolean;
}

export interface WalmartProductRequest {
  product_id: string;
  include_analysis?: boolean;
}

export interface ProductScrapingResponse extends AnalysisMetrics {
  product_info?: {
    title?: string;
    url?: string;
    rating?: number;
    review_count?: number;
  };
  reviews: ProductReview[];
  results: BatchReviewResult[];
  scraping_time: number;
  processing_time: number;
}

// ==================== UI Component Props ====================

export interface TrustLevelBadgeProps {
  trustLevel: TrustLevel;
  size?: 'sm' | 'md' | 'lg';
  showPercentage?: boolean;
}

export interface ResultsTableProps {
  results: BatchReviewResult[];
  onFilter?: (prediction?: 0 | 1) => void;
  onExport?: () => void;
  isLoading?: boolean;
}

export interface AnalysisCardProps {
  title: string;
  children: React.ReactNode;
  icon?: React.ReactNode;
  variant?: 'primary' | 'secondary';
}

export interface LoadingStateProps {
  message?: string;
  progress?: number;
}

export interface ErrorStateProps {
  error: string;
  onRetry?: () => void;
}

// ==================== Application State Types ====================

export interface AppState {
  isDarkMode: boolean;
  selectedModel?: string;
  useEnsemble: boolean;
  isAnalyzing: boolean;
  error?: string;
}

export interface AnalysisState<T = PredictionResult | AnalysisMetrics | BatchAnalysisResponse | ProductScrapingResponse> {
  isLoading: boolean;
  error?: string;
  result?: T;
  progress?: number;
}

// ==================== API Configuration ====================

export interface APIConfig {
  baseURL: string;
  timeout: number;
  retries: number;
  headers?: Record<string, string>;
}

// ==================== Form Types ====================

export interface SingleReviewFormData {
  reviewText: string;
}

export interface CSVUploadFormData {
  file: File;
  columnName: string;
}

export interface ProductFormData {
  productUrl?: string;
  productId?: string;
}

// ==================== Utility Types ====================

export interface APIError {
  status: number;
  message: string;
  details?: unknown;
}

export interface PaginationState {
  currentPage: number;
  pageSize: number;
  total: number;
}

export interface FilterState {
  prediction?: 0 | 1;
  confidenceRange?: [number, number];
  searchTerm?: string;
}
