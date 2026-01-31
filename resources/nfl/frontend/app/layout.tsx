import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'NFL AI Coach - Data-Driven Decision Support',
  description: 'Real-time coaching decisions powered by AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
