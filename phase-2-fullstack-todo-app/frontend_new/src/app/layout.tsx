import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from './Header';
import Footer from './Footer';

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Task Manager Pro - Organize Your Tasks",
  description: "A simple and effective task management application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <Header />
          <main className="flex-grow">
            {children}
          </main>
          <Footer />
        </div>
      </body>
    </html>
  );
}
