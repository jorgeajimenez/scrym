import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NFL AI Coach - Ultimate",
  description: "Next.js implementation of the mockup",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className='font-sans'>
        {children}
      </body>
    </html>
  );
}
