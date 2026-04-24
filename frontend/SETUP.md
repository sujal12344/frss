# 🚀 Fake Review Detection - Frontend Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
pnpm install
```

### 2. Configure Environment
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8501
```

### 3. Run Development Server
```bash
pnpm dev
```

Visit: http://localhost:3000

## 📂 Complete Project Structure

```
frontend/
├── .env.example              # Environment variable template
├── .env.local               # Your environment variables (create from .env.example)
├── .gitignore               # Git ignore rules
├── README.md                # Full project documentation
├── package.json             # Dependencies & scripts
├── tsconfig.json            # TypeScript configuration
├── next.config.ts           # Next.js configuration
├── tailwind.config.ts       # Tailwind CSS configuration
├── postcss.config.mjs       # PostCSS configuration
│
├── public/                  # Static assets (images, icons, etc.)
│
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx       # ✅ Root layout with ThemeProvider
│   │   ├── page.tsx         # ✅ Home page (beautiful landing page)
│   │   ├── globals.css      # Global styles
│   │   │
│   │   └── analysis/        # Analysis pages group
│   │       ├── layout.tsx   # ✅ Navigation layout
│   │       │
│   │       ├── single-review/
│   │       │   └── page.tsx # ✅ Single review analysis
│   │       │
│   │       ├── csv-batch/
│   │       │   └── page.tsx # ✅ CSV batch processing
│   │       │
│   │       ├── amazon-product/
│   │       │   └── page.tsx # ✅ Amazon product scraping
│   │       │
│   │       └── walmart-product/
│   │           └── page.tsx # ✅ Walmart product scraping
│   │
│   ├── components/
│   │   └── shared.tsx       # ✅ Reusable UI components
│   │       - TrustLevelBadge
│   │       - PredictionBadge
│   │       - LoadingState
│   │       - ErrorState
│   │       - MetricsCard
│   │       - ResultsTable
│   │       - Card
│   │       - ThemeToggle
│   │
│   └── lib/
│       ├── types.ts         # ✅ TypeScript types & interfaces
│       ├── api.ts           # ✅ API service layer
│       │
│       ├── context/
│       │   └── ThemeContext.tsx  # ✅ Dark/light mode context
│       │
│       └── hooks/
│           └── useAnalysis.ts    # ✅ Custom analysis hooks
│               - useSingleReviewAnalysis()
│               - useBatchAnalysis()
│               - useAmazonAnalysis()
│               - useWalmartAnalysis()
```

## ✅ Completed Files

### Core Setup (4 files)
- ✅ `src/app/layout.tsx` - Root layout with theme provider
- ✅ `src/app/page.tsx` - Beautiful home page with hero section
- ✅ `src/lib/types.ts` - Comprehensive TypeScript types (~200 lines)
- ✅ `src/app/globals.css` - Enhanced global styles

### API & Services (2 files)
- ✅ `src/lib/api.ts` - Centralized API service with retry logic
- ✅ `src/lib/context/ThemeContext.tsx` - Dark/light mode provider

### Hooks & State (1 file)
- ✅ `src/lib/hooks/useAnalysis.ts` - All 4 analysis hooks

### Components (1 file)
- ✅ `src/components/shared.tsx` - 8 reusable components

### Pages (5 files)
- ✅ `src/app/analysis/layout.tsx` - Navigation layout
- ✅ `src/app/analysis/single-review/page.tsx` - Single review
- ✅ `src/app/analysis/csv-batch/page.tsx` - CSV batch processing
- ✅ `src/app/analysis/amazon-product/page.tsx` - Amazon scraping
- ✅ `src/app/analysis/walmart-product/page.tsx` - Walmart scraping

### Documentation & Config (3 files)
- ✅ `README.md` - Full project documentation
- ✅ `.env.example` - Environment template
- ✅ `SETUP.md` - This file!

## 🎯 Key Features Implemented

### 1. **Modular Architecture** ✅
- Separated concerns (API, hooks, components, pages)
- Reusable components with TypeScript
- Custom hooks for state management
- Centralized API service layer

### 2. **Type Safety** ✅
- Full TypeScript coverage
- Strong typing for all API interactions
- Component prop validation
- Error type definitions

### 3. **State Management** ✅
- React Context for theme
- Custom hooks for analysis state
- Loading states with progress tracking
- Error handling and recovery

### 4. **User Interface** ✅
- Beautiful home page with hero section
- 4 dedicated analysis pages
- Responsive design (mobile-first)
- Dark mode support
- Animations & transitions

### 5. **API Integration** ✅
- Retry logic with exponential backoff
- Error normalization
- Timeout management
- Network error handling

### 6. **Best Practices** ✅
- Clean code structure
- Comprehensive comments
- Consistent naming conventions
- Accessibility compliance
- SEO-friendly

## 🔧 Development Commands

```bash
# Development
pnpm dev          # Start dev server on localhost:3000

# Building
pnpm build        # Build for production
pnpm start        # Run production build

# Code Quality
pnpm lint         # Run ESLint
```

## 📡 API Integration Points

The frontend expects these backend endpoints:

### 1. Single Review Analysis
```javascript
POST /api/analyze-review
Body: { review_text: string, use_ensemble?: boolean }
```

### 2. Batch Processing
```javascript
POST /api/analyze-batch
Body: FormData { file, column_name }
```

### 3. Amazon Analysis
```javascript
POST /api/analyze-amazon-product
Body: { product_url: string }
```

### 4. Walmart Analysis
```javascript
POST /api/analyze-walmart-product
Body: { product_id: string }
```

## 🎨 Styling & Customization

### Tailwind CSS
- Utility-first CSS framework
- Fully configured with dark mode
- Custom animations included
- Responsive breakpoints: sm, md, lg, xl

### Dark Mode
- Automatic detection of system preference
- Persistent localStorage
- Smooth transitions
- CSS class-based (`.dark:` prefix)

### Colors
- Primary: Blue (#3b82f6)
- Secondary: Cyan (#06b6d4)
- Success: Green (#10b981)
- Danger: Red (#ef4444)
- Warning: Yellow (#f59e0b)

## 🧪 Testing the Application

### 1. Test Home Page
```
Visit: http://localhost:3000
Expected: Beautiful home page with feature cards and CTA
```

### 2. Test Single Review
```
1. Navigate to "Single Review" tab
2. Enter review text
3. Click "Analyze Review"
4. Should show prediction results
```

### 3. Test Dark Mode
```
1. Click theme toggle (☀️/🌙) in navigation
2. Page should switch to dark mode
3. Reload page - dark mode should persist
```

## 📝 Code Organization Principles

### 1. **Separation of Concerns**
- API logic in `lib/api.ts`
- State logic in hooks
- UI logic in components
- Type definitions centralized

### 2. **Reusability**
- Generic components
- Custom hooks
- Shared utilities
- No duplication

### 3. **Maintainability**
- Clear file structure
- Descriptive names
- Comments for complex logic
- Error handling everywhere

### 4. **Scalability**
- Easy to add new pages
- Extensible hook system
- Modular components
- Centralized configuration

## 🚨 Troubleshooting

### Issue: "Cannot find module 'X'"
**Solution**: Run `pnpm install` and restart dev server

### Issue: API returns 404
**Solution**: Check `NEXT_PUBLIC_API_URL` in `.env.local`

### Issue: Dark mode doesn't work
**Solution**: Clear cache/localStorage and reload

### Issue: Pages not loading
**Solution**: Check browser console for TypeScript errors

## 📚 Further Customization

### Add New Page
1. Create folder: `src/app/analysis/[name]/`
2. Create file: `page.tsx`
3. Update navigation in `layout.tsx`

### Add New Component
1. Create file: `src/components/[name].tsx`
2. Export from `shared.tsx`
3. Use in pages

### Add New API Endpoint
1. Add type in `src/lib/types.ts`
2. Add function in `src/lib/api.ts`
3. Add hook in `src/lib/hooks/useAnalysis.ts`

## 🎓 Learning Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Web Accessibility](https://www.w3.org/WAI/)

## ✨ What's Next?

After setup, you can:
1. ✅ Run the development server
2. ✅ Test all pages and features
3. ✅ Configure your backend API URL
4. ✅ Customize colors and branding
5. ✅ Add additional features as needed

## 📞 Support

For issues or questions:
1. Check this guide
2. Check README.md
3. Review code comments
4. Check browser console for errors

---

**Happy coding! 🎉**

Built with ❤️ using Next.js, React, TypeScript, and Tailwind CSS.
