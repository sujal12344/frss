'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ThemeToggle } from '@/components/shared';

export default function Home() {
  const [hoveredFeature, setHoveredFeature] = useState<number | null>(null);

  const features = [
    {
      icon: '📝',
      title: 'Single Review Analysis',
      description: 'Analyze individual reviews with detailed predictions and confidence scores using our ensemble ML models.',
      href: '/analysis/single-review',
      gradient: 'from-blue-500 to-cyan-500',
    },
    {
      icon: '📊',
      title: 'Batch CSV Analysis',
      description: 'Upload CSV files with multiple reviews for bulk analysis. Get comprehensive statistics and distribution insights.',
      href: '/analysis/csv-batch',
      gradient: 'from-purple-500 to-pink-500',
    },
    {
      icon: '🛍️',
      title: 'Amazon Products',
      description: 'Scrape and analyze all reviews from Amazon product pages. Detect fake reviews at scale.',
      href: '/analysis/amazon-product',
      gradient: 'from-orange-500 to-red-500',
    },
    {
      icon: '🏪',
      title: 'Walmart Products',
      description: 'Scrape and analyze reviews from Walmart products. Get authenticity ratings and trust levels.',
      href: '/analysis/walmart-product',
      gradient: 'from-blue-600 to-blue-400',
    },
  ];

  const stats = [
    { label: 'ML Models', value: '5+', icon: '🤖' },
    { label: 'Review Capacity', value: '∞', icon: '📈' },
    { label: 'Trust Levels', value: '12', icon: '⭐' },
    { label: 'Accuracy', value: '94%+', icon: '🎯' },
  ];

  return (
    <>
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
          <div className="flex items-center gap-2 text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
            🔍 FakeReview.AI
          </div>
          <ThemeToggle />
        </div>
      </nav>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative overflow-hidden bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800 py-20 px-4">
          {/* Background decoration */}
          <div className="absolute inset-0 overflow-hidden">
            <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 dark:bg-blue-900 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
            <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-200 dark:bg-purple-900 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
          </div>

          <div className="relative max-w-7xl mx-auto text-center z-10">
            <div className="inline-block mb-4 px-4 py-2 bg-blue-100 dark:bg-blue-900/30 rounded-full border border-blue-200 dark:border-blue-800">
              <p className="text-sm font-semibold text-blue-600 dark:text-blue-400">🚀 AI-Powered Fake Review Detection</p>
            </div>

            <h1 className="text-5xl sm:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Detect Fake Reviews with Confidence
            </h1>

            <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto leading-relaxed">
              Leverage advanced machine learning models to identify fake reviews across multiple platforms. Get detailed analysis, trust scores, and actionable insights in seconds.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/analysis/single-review"
                className="px-8 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all hover:scale-105"
              >
                Start Analyzing →
              </Link>
              <a
                href="#features"
                className="px-8 py-3 border-2 border-blue-600 dark:border-blue-400 text-blue-600 dark:text-blue-400 font-semibold rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
              >
                Learn More
              </a>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16 px-4 max-w-7xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {stats.map((stat, idx) => (
              <div
                key={idx}
                className="p-6 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-lg text-center hover:shadow-md transition-shadow"
              >
                <div className="text-4xl mb-2">{stat.icon}</div>
                <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">{stat.value}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-20 px-4 bg-gray-50 dark:bg-gray-800/50">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4">Powerful Analysis Tools</h2>
              <p className="text-gray-600 dark:text-gray-400">Choose the perfect tool for your fake review detection needs</p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {features.map((feature, idx) => (
                <Link
                  key={idx}
                  href={feature.href}
                  onMouseEnter={() => setHoveredFeature(idx)}
                  onMouseLeave={() => setHoveredFeature(null)}
                  className="group relative overflow-hidden"
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                  <div className={`p-8 h-full bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl transition-all duration-300 ${
                    hoveredFeature === idx ? 'shadow-xl scale-105 -translate-y-1' : 'shadow-md hover:shadow-lg'
                  }`}>
                    <div className="flex items-start gap-4 mb-4">
                      <div className={`text-4xl p-3 rounded-lg bg-gradient-to-r ${feature.gradient} text-white flex-shrink-0`}>
                        {feature.icon}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-semibold mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                          {feature.title}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">{feature.description}</p>
                      </div>
                    </div>
                    <div className="flex items-center text-blue-600 dark:text-blue-400 font-semibold text-sm group-hover:translate-x-2 transition-transform">
                      Get Started →
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="py-20 px-4">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-4xl font-bold text-center mb-16">How It Works</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  step: '1',
                  title: 'Input Data',
                  description: 'Provide a review, upload CSV file, or enter product URL',
                  icon: '📥',
                },
                {
                  step: '2',
                  title: 'AI Analysis',
                  description: 'Our ensemble ML models analyze the text for fake patterns',
                  icon: '🧠',
                },
                {
                  step: '3',
                  title: 'Get Results',
                  description: 'Receive detailed predictions with trust levels and confidence scores',
                  icon: '📊',
                },
              ].map((item, idx) => (
                <div key={idx} className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 text-white text-2xl rounded-full font-bold mb-4">
                    {item.step}
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                  <p className="text-gray-600 dark:text-gray-400">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4 bg-gradient-to-r from-blue-600 to-cyan-600">
          <div className="max-w-4xl mx-auto text-center text-white">
            <h2 className="text-4xl font-bold mb-4">Ready to Detect Fake Reviews?</h2>
            <p className="text-lg mb-8 opacity-90">Start analyzing reviews instantly with our AI-powered detection system</p>
            <Link
              href="/analysis/single-review"
              className="inline-block px-8 py-4 bg-white text-blue-600 font-bold rounded-lg hover:shadow-lg transition-all hover:scale-105"
            >
              Begin Analysis Now →
            </Link>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <p>© 2026 Fake Review Detection. All rights reserved.</p>
          <p className="text-sm mt-2">Built with Next.js, Machine Learning, and ❤️</p>
        </div>
      </footer>

      <style jsx>{`
        @keyframes blob {
          0%, 100% { transform: translate(0, 0) scale(1); }
          33% { transform: translate(30px, -50px) scale(1.1); }
          66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        .animate-blob {
          animation: blob 7s infinite;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
      `}</style>
    </>
  );
}
