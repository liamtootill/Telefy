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
  title: "Telefy",
  description: "Telefy is your AI agent for Telegram, powered by Solana.",
  icons: {
    icon: "/images/logo/logo_5.png",
  },
  openGraph: {
    title: "Telefy",
    description: "Telefy is your AI agent for Telegram, powered by Solana.",
    url: "https://telefy.xyz/",
    siteName: "Telefy",
    images: [
      {
        url: "/images/banner-twitter/banner twitter.png",
        width: 512,
        height: 512,
        alt: "Telefy Logo",
      },
    ],
    type: "website",
    locale: "en_US",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="bg-gray-100">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-gray-100`}
      >
        {children}
      </body>
    </html>
  );
}
