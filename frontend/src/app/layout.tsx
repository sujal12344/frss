import { ThemeProvider } from "@/lib/context/ThemeContext";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Fake Review Detection - AI-Powered Analysis",
  description:
    "Detect fake reviews with advanced ML models. Analyze single reviews, batch CSV files, and product reviews from Amazon & Walmart.",
  keywords: ["fake reviews", "detection", "machine learning", "analysis"],
  authors: [{ name: "Fake Review Detection Team" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable}`}
    >
      <head />
      <body className="min-h-full flex flex-col bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors antialiased">
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
