# Fake Review Detection - Next.js Frontend

A production-ready Next.js frontend for the Fake Review Detection system. Built with TypeScript, Tailwind CSS, and best practices for modularity, maintainability, and reusability.

## 🚀 Project Overview

This Next.js application provides a comprehensive UI for analyzing reviews using advanced ML models. It supports:

- **Single Review Analysis**: Analyze individual reviews with detailed predictions
- **Batch CSV Processing**: Upload and analyze multiple reviews at once
- **Amazon Product Scraping**: Scrape and analyze all reviews from Amazon products
- **Walmart Product Scraping**: Scrape and analyze all reviews from Walmart products

## 📁 Project Structure

```
src/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with ThemeProvider
│   ├── page.tsx                 # Home page with hero and features
│   ├── globals.css              # Global styles
│   └── analysis/                # Analysis pages group
│       ├── layout.tsx           # Analysis pages layout with navigation
│       ├── single-review/       # Single review analysis
│       │   └── page.tsx
│       ├── csv-batch/           # CSV batch processing
│       │   └── page.tsx
│       ├── amazon-product/      # Amazon product analysis
│       │   └── page.tsx
│       └── walmart-product/     # Walmart product analysis
│           └── page.tsx
│
├── components/
│   └── shared.tsx               # Reusable UI components
│       ├── TrustLevelBadge
│       ├── PredictionBadge
│       ├── LoadingState
│       ├── ErrorState
│       ├── MetricsCard
│       ├── ResultsTable
│       ├── Card
│       └── ThemeToggle
│
├── lib/
│   ├── types.ts                 # TypeScript interfaces & types
│   ├── api.ts                   # API service layer
│   ├── context/
│   │   └── ThemeContext.tsx     # Theme management (dark/light)
│   └── hooks/
│       └── useAnalysis.ts       # Custom analysis hooks
│           ├── useSingleReviewAnalysis
│           ├── useBatchAnalysis
│           ├── useAmazonAnalysis
│           └── useWalmartAnalysis
│
└── public/                       # Static assets
```

## 🏗️ Architecture & Design Patterns

### 1. **Component Architecture**
- **Shared Components**: Reusable UI components (`TrustLevelBadge`, `MetricsCard`, `Card`, etc.)
- **Page Components**: Feature-specific analysis pages
- **Layout Components**: Navigation and structure
- All components use TypeScript for type safety

### 2. **API Layer**
- **Centralized API Service** (`lib/api.ts`):
  - Handles all backend communication
  - Includes retry logic with exponential backoff
  - Error handling and normalization
  - Request/response typing
  - Timeout management

### 3. **State Management**
- **React Context**: Theme/Dark mode management (`ThemeContext`)
- **Custom Hooks**: Analysis state logic (`useAnalysis.ts`)
  - Separate hooks for each analysis type
  - Loading states, error handling, progress tracking
  - Reusable across multiple components

### 4. **Type Safety**
- **Comprehensive TypeScript Types** (`lib/types.ts`):
  - API request/response types
  - Component prop types
  - UI state types
  - Utility types
  - Full type coverage for backend integration

### 5. **Styling**
- **Tailwind CSS**: Utility-first CSS framework
- **Dark Mode**: CSS classes-based (`.dark`)
- **Responsive**: Mobile-first design
- **Animations**: Custom CSS animations for UX polish
- **Accessibility**: Focus states and ARIA labels

## 🔧 Setup & Installation

### Prerequisites
- Node.js 18+ (or use with pnpm)
- pnpm (package manager)

### Installation

```bash
# Install dependencies
pnpm install

# Create .env.local file
cp .env.example .env.local

# Update API URL in .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8501
```

### Environment Variables

Create `.env.local` file:

```env
# Backend API configuration
NEXT_PUBLIC_API_URL=http://localhost:8501
# or change to your Streamlit backend URL
```

## 🚀 Running the Application

### Development Mode
```bash
pnpm dev
```
Open [http://localhost:3000](http://localhost:3000)

### Production Build
```bash
pnpm build
pnpm start
```

## 📊 Features & Components

### Pages

1. **Home Page** (`/`)
   - Hero section with CTA
   - Feature cards
   - Statistics display
   - How it works section
   - Navigation to analysis tools

2. **Single Review Analysis** (`/analysis/single-review`)
   - Text input for review
   - Ensemble model toggle
   - Real-time analysis results
   - Model-by-model predictions
   - Confidence scores

3. **Batch CSV Analysis** (`/analysis/csv-batch`)
   - File upload with drag-and-drop
   - Column name configuration
   - Progress tracking
   - Results table with filtering
   - Export to CSV

4. **Amazon Product Analysis** (`/analysis/amazon-product`)
   - Product URL input
   - Web scraping progress
   - Product information display
   - Review distribution analysis
   - Trust level assessment

5. **Walmart Product Analysis** (`/analysis/walmart-product`)
   - Product ID input
   - Web scraping progress
   - Product information display
   - Review distribution analysis
   - Trust level assessment

### Reusable Components

- **TrustLevelBadge**: Display trust level with color coding
- **PredictionBadge**: Show prediction (Genuine/Fake) with confidence
- **MetricsCard**: Display key metrics with icons
- **ResultsTable**: Filterable results table
- **LoadingState**: Loading indicator with progress bar
- **ErrorState**: Error display with retry option
- **Card**: Generic card container
- **ThemeToggle**: Dark/light mode toggle button

### Custom Hooks

- **useSingleReviewAnalysis()**: Manage single review analysis state
- **useBatchAnalysis()**: Manage batch processing with progress
- **useAmazonAnalysis()**: Manage Amazon product scraping
- **useWalmartAnalysis()**: Manage Walmart product scraping

All hooks include:
- Loading states
- Error handling
- Progress tracking
- Automatic API calls
- Result caching-ready structure

## 🎨 Styling & Theme

### Dark Mode
- Automatic preference detection
- LocalStorage persistence
- CSS class-based (`dark:` Tailwind prefix)
- Smooth transitions

### Responsive Design
- Mobile-first approach
- Breakpoints: `sm`, `md`, `lg`, `xl`
- Flexible grid layouts
- Touch-friendly UI

### Animations
- Smooth page transitions
- Blob animations (background)
- Fade-in and slide-in effects
- Hover animations
- Loading spinners

## 🔌 API Integration

### Backend API Endpoints Expected

```typescript
// Single Review
POST /api/analyze-review
Request: { review_text: string, use_ensemble?: boolean }
Response: SingleReviewResponse

// Batch Processing
POST /api/analyze-batch
Body: FormData (file + column_name)
Response: BatchAnalysisResponse

// Product Scraping
POST /api/analyze-amazon-product
Request: { product_url: string }
Response: ProductScrapingResponse

POST /api/analyze-walmart-product
Request: { product_id: string }
Response: ProductScrapingResponse

// Health Check
GET /api/health
Response: boolean

// Model Info
GET /api/models-info
Response: { models: string[], metrics: Record<string, unknown> }

// Trust Levels
GET /api/trust-levels
Response: Record<string, TrustLevel>
```

### API Features
- Automatic retry with exponential backoff (3 retries)
- 60-second timeout per request
- Error normalization
- Network error handling
- Graceful degradation

## 📦 Dependencies

### Core
- **next**: ^16.2.4 - React framework
- **react**: ^19 - UI library
- **typescript**: ^5 - Type safety

### Styling
- **tailwindcss**: ^3 - CSS framework
- **postcss**: ^8 - CSS processing

### Development
- **eslint**: ^9 - Code linting

## 🧪 Best Practices Implemented

### 1. **Type Safety**
✅ Full TypeScript coverage
✅ Strong typing for API responses
✅ Component prop validation
✅ Type-safe hooks

### 2. **Code Organization**
✅ Separation of concerns
✅ Modular component structure
✅ Centralized API layer
✅ Reusable utilities

### 3. **Performance**
✅ Code splitting (App Router)
✅ Image optimization
✅ CSS bundling
✅ Lazy loading components

### 4. **Accessibility**
✅ ARIA labels
✅ Focus management
✅ Color contrast compliance
✅ Keyboard navigation

### 5. **Maintainability**
✅ Clear file structure
✅ Consistent naming conventions
✅ Comprehensive comments
✅ Error handling throughout

### 6. **Scalability**
✅ Modular architecture
✅ Easy to add new pages
✅ Extensible hooks system
✅ Centralized configuration

## 🚀 Future Enhancements

- [ ] Add result charts and visualizations
- [ ] Implement result export to multiple formats (PDF, Excel)
- [ ] Add user authentication
- [ ] Implement caching for repeat analyses
- [ ] Add real-time analysis progress notifications
- [ ] Build mobile app version
- [ ] Add API rate limiting UI
- [ ] Implement analysis history

## 📝 Development Notes

### Adding New Analysis Types

1. Create new hook in `lib/hooks/useAnalysis.ts`
2. Create new page in `app/analysis/[type]/page.tsx`
3. Add API endpoint to `lib/api.ts`
4. Add types to `lib/types.ts`
5. Update navigation in layout

### Adding New Components

1. Create component in `components/`
2. Export from barrel file
3. Add TypeScript props interface
4. Include usage examples in comments
5. Ensure accessibility compliance

### Updating API Integration

1. Update types in `lib/types.ts`
2. Add/modify API calls in `lib/api.ts`
3. Update hooks to match new response format
4. Test with mock data first

## 🐛 Troubleshooting

### API Connection Issues
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Ensure backend is running
- Check CORS settings on backend
- Verify network connectivity

### Theme Not Persisting
- Check localStorage permissions
- Clear browser cache
- Verify ThemeProvider is in layout

### Components Not Rendering
- Check TypeScript compilation errors
- Verify imports are correct
- Ensure components are exported
- Check browser console for errors

## 📄 License

This project is part of the Fake Review Detection system.

## 👨‍💻 Development Workflow

```bash
# Start development
pnpm dev

# Build for production
pnpm build

# Run production build
pnpm start

# Lint code
pnpm lint
```

## 📧 Support

For issues, questions, or suggestions, please reach out to the team.
