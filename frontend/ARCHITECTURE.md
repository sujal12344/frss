# 🏗️ Frontend Architecture Documentation

## Overview

The Fake Review Detection frontend is built with Next.js using a modular, scalable architecture. This document explains the design decisions, patterns, and best practices used.

## Architecture Layers

```
┌─────────────────────────────────────────────┐
│           Presentation Layer                │
│  (Pages, Components, User Interactions)     │
├─────────────────────────────────────────────┤
│        Business Logic Layer                 │
│  (Custom Hooks, State Management, Context)  │
├─────────────────────────────────────────────┤
│           Service Layer                     │
│  (API Calls, Error Handling, Retry Logic)   │
├─────────────────────────────────────────────┤
│             Backend API                     │
│  (Streamlit Python Server)                  │
└─────────────────────────────────────────────┘
```

## Layer Details

### 1. Presentation Layer

**Location**: `src/app/`, `src/components/`

**Components**:
- **Pages**: Full-page components under `src/app/`
- **Shared Components**: Reusable UI components in `src/components/shared.tsx`
- **Layouts**: Route group layouts for organization

**Key Files**:
- `src/app/page.tsx` - Home/landing page
- `src/app/analysis/single-review/page.tsx` - Single review analysis
- `src/app/analysis/csv-batch/page.tsx` - Batch processing
- `src/app/analysis/amazon-product/page.tsx` - Amazon scraping
- `src/app/analysis/walmart-product/page.tsx` - Walmart scraping

**Characteristics**:
- Client-side components (`'use client'`)
- React hooks for state management
- TypeScript for type safety
- Responsive design with Tailwind
- Accessibility built-in

### 2. Business Logic Layer

**Location**: `src/lib/hooks/`, `src/lib/context/`

#### 2.1 Custom Hooks (`useAnalysis.ts`)

```typescript
// Each hook manages specific analysis workflow
useSingleReviewAnalysis()      // Single review logic
useBatchAnalysis()             // Batch processing logic
useAmazonAnalysis()            // Amazon scraping logic
useWalmartAnalysis()           // Walmart scraping logic
```

**Hook Pattern**:
```typescript
export function useAnalyzerHook() {
  const [state, setState] = useState<AnalysisState>({
    isLoading: false,
  });

  const analyze = useCallback(async (input) => {
    setState({ isLoading: true });
    try {
      const result = await api.analyzeFunction(input);
      setState({ isLoading: false, result });
      return result;
    } catch (error) {
      setState({ isLoading: false, error });
      throw error;
    }
  }, []);

  const reset = useCallback(() => {
    setState({ isLoading: false });
  }, []);

  return { ...state, analyze, reset };
}
```

**Benefits**:
- Reusable state logic
- Testable logic
- Separation from UI
- Consistent error handling

#### 2.2 Context Management (`ThemeContext.tsx`)

**Purpose**: Global theme state management

**Pattern**:
```typescript
// Create context
const ThemeContext = createContext<ThemeContextType>();

// Provider component
export function ThemeProvider({ children }) {
  const [isDarkMode, setIsDarkMode] = useState(false);
  // ...
}

// Custom hook to use context
export function useTheme() {
  return useContext(ThemeContext);
}
```

**Benefits**:
- Global state without props drilling
- Clean API with custom hook
- Persistent theme state

### 3. Service Layer

**Location**: `src/lib/api.ts`

**Responsibility**: Handle all backend communication

#### 3.1 Core Functions

```typescript
// Single endpoints
analyzeReview(request)
analyzeBatch(file, columnName)
analyzeAmazonProduct(request)
analyzeWalmartProduct(request)

// Utility endpoints
getModelsInfo()
getTrustLevels()
healthCheck()
```

#### 3.2 Retry Logic

```typescript
async function fetchWithRetry(url, options, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      // Attempt request
      return response;
    } catch (error) {
      if (shouldNotRetry(error)) throw error;
      await delay(exponentialBackoff(i)); // 1s, 2s, 4s
    }
  }
}
```

#### 3.3 Error Handling

```typescript
class APIError extends Error {
  constructor(status, message, details) {
    super(message);
    this.status = status;
    this.details = details;
  }
}

function handleAPIError(error) {
  if (error instanceof APIError) return error;
  if (error.message === 'Failed to fetch') {
    return new APIError(0, 'Network error');
  }
  return new APIError(500, error.message);
}
```

**Benefits**:
- Single responsibility
- Retry on transient failures
- Standardized error handling
- Timeout management

## Data Flow

### Example: Single Review Analysis

```
┌─────────────────────────────────┐
│   User enters review text       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  useSingleReviewAnalysis()      │
│  - Manages state                │
│  - Calls analyze()              │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  api.analyzeReview()            │
│  - Calls backend                │
│  - Retries on failure           │
│  - Returns typed response       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Backend API /analyze-review    │
│  - Processes review             │
│  - Returns prediction           │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│  Component renders results      │
│  - Shows prediction             │
│  - Shows confidence             │
│  - Shows models breakdown       │
└─────────────────────────────────┘
```

## Component Hierarchy

```
<html>
  ├── <RootLayout>
  │   ├── <ThemeProvider>
  │   │   └── {children}
  │   │       ├── <HomePage>
  │   │       └── <AnalysisLayout>
  │   │           ├── <Navigation>
  │   │           ├── <SingleReviewPage>
  │   │           │   ├── <Card>
  │   │           │   ├── <Form>
  │   │           │   ├── <LoadingState>
  │   │           │   ├── <ResultsDisplay>
  │   │           │   │   ├── <PredictionBadge>
  │   │           │   │   ├── <TrustLevelBadge>
  │   │           │   │   └── <MetricsCard>
  │   │           │   └── <ErrorState>
  │   │           │
  │   │           ├── <BatchAnalysisPage>
  │   │           │   ├── <FileUpload>
  │   │           │   ├── <ProgressBar>
  │   │           │   ├── <ResultsTable>
  │   │           │   └── <ExportButton>
  │   │           │
  │   │           ├── <AmazonProductPage>
  │   │           │   ├── <URLInput>
  │   │           │   ├── <ProductInfo>
  │   │           │   ├── <ResultsDisplay>
  │   │           │   └── <StatisticsCard>
  │   │           │
  │   │           └── <WalmartProductPage>
  │   │               └── ... (similar structure)
  │   │
  │   └── <Footer>
  │
  └── </RootLayout>
```

## State Management Strategy

### 1. Local Component State
```typescript
// For UI-only state (toggles, forms, local UI)
const [reviewText, setReviewText] = useState('');
const [activeTab, setActiveTab] = useState('single-review');
```

### 2. Hook State
```typescript
// For business logic state (analysis results, loading)
const { isLoading, error, result, analyze } = useAnalysis();
```

### 3. Context State
```typescript
// For global state (theme, user preferences)
const { isDarkMode, toggleDarkMode } = useTheme();
```

### State Flow Rule
```
UI State (Local) → Business State (Hooks) → Global State (Context)
```

## Type Safety Strategy

### 1. Type Definition Layers

```typescript
// API Types - What backend returns
interface SingleReviewResponse {
  prediction: 0 | 1;
  confidence: number;
  // ...
}

// Component Types - What component needs
interface ResultsDisplayProps {
  result: SingleReviewResponse;
  isLoading: boolean;
}

// Hook Types - What hook manages
interface AnalysisState {
  isLoading: boolean;
  error?: string;
  result?: SingleReviewResponse;
}
```

### 2. Generic Type Parameters
```typescript
// Reusable component with generic types
interface CardProps<T> {
  data: T;
  render: (item: T) => React.ReactNode;
}

// Reusable hook with generic response
function useAPICall<T>(url: string): {
  data: T;
  loading: boolean;
  error: Error | null;
}
```

## Error Handling Pattern

### 1. API Level
```typescript
try {
  return await fetch(url);
} catch (error) {
  throw new APIError(status, message);
}
```

### 2. Hook Level
```typescript
try {
  const result = await api.call();
  setState({ isLoading: false, result });
} catch (error) {
  setState({ isLoading: false, error });
  throw error;
}
```

### 3. Component Level
```typescript
{error && (
  <ErrorState 
    error={error} 
    onRetry={() => analyze(data)}
  />
)}
```

## Performance Optimization

### 1. Code Splitting
- Next.js App Router automatically splits code
- Route segments loaded on-demand

### 2. Memoization
```typescript
// Memoize expensive computations
const memoizedValue = useMemo(() => {
  return expensiveComputation(data);
}, [data]);

// Memoize callbacks
const memoizedCallback = useCallback(() => {
  doSomething(value);
}, [value]);
```

### 3. Dynamic Imports
```typescript
// Load components only when needed
const HeavyComponent = dynamic(() => import('../components/Heavy'));
```

## Accessibility Considerations

### 1. Semantic HTML
```typescript
<button>Analyze</button>
<form>
  <input type="text" />
</form>
```

### 2. ARIA Labels
```typescript
<button aria-label="Toggle dark mode">
  {isDarkMode ? '☀️' : '🌙'}
</button>
```

### 3. Focus Management
```typescript
<input className="focus:ring-2 focus:ring-blue-500" />
```

### 4. Color Contrast
- Text: WCAG AA compliant
- Interactive elements: Visible focus states

## Testing Strategy

### 1. Unit Tests
- Test hooks in isolation
- Test utility functions
- Test type definitions

### 2. Component Tests
- Test component rendering
- Test user interactions
- Test error states

### 3. Integration Tests
- Test full page workflows
- Test API integration
- Test dark mode persistence

## Scalability Patterns

### Adding New Analysis Type

1. **Create Type**
   ```typescript
   interface NewAnalysisResponse extends AnalysisMetrics {
     // ...
   }
   ```

2. **Create Hook**
   ```typescript
   export function useNewAnalysis() {
     const [state, setState] = useState();
     const analyze = useCallback(async (input) => {
       // ...
     }, []);
     return { ...state, analyze };
   }
   ```

3. **Create API Function**
   ```typescript
   export async function analyzeNew(request) {
     return fetchWithRetry(`${API_BASE_URL}/api/analyze-new`, {
       method: 'POST',
       body: JSON.stringify(request),
     });
   }
   ```

4. **Create Page**
   ```typescript
   export default function NewAnalysisPage() {
     const { isLoading, result, analyze } = useNewAnalysis();
     // ...
   }
   ```

5. **Update Navigation**
   - Add route to layout navigation

## Dependencies & Why

- **next**: App Router, SSR capabilities
- **react**: Component model, hooks
- **typescript**: Type safety, developer experience
- **tailwindcss**: Responsive design, dark mode support
- **postcss**: CSS processing

## Configuration Files

- `tsconfig.json` - TypeScript settings
- `next.config.ts` - Next.js configuration
- `tailwind.config.ts` - Tailwind CSS customization
- `postcss.config.mjs` - PostCSS plugins
- `eslint.config.mjs` - ESLint rules

## Deployment Considerations

### 1. Environment Variables
- API URL configuration
- Feature flags
- Analytics keys

### 2. Build Optimization
- Tree-shaking unused code
- Image optimization
- CSS minification

### 3. Performance
- CDN for static assets
- Database caching
- API response caching

## Summary

This architecture provides:
- ✅ Clear separation of concerns
- ✅ Type safety with TypeScript
- ✅ Reusable components and hooks
- ✅ Scalable structure
- ✅ Easy to test
- ✅ Maintainable code
- ✅ Best practices throughout

---

**Next**: Read [SETUP.md](SETUP.md) for quick-start instructions or [README.md](README.md) for comprehensive documentation.
