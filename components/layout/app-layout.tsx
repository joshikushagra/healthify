"use client"

import type React from "react"
import { useState } from "react"
import { ThemeProvider } from "next-themes"
import { Sidebar } from "./sidebar"
import { Navbar } from "./navbar"

interface AppLayoutProps {
  children: React.ReactNode
  userType: "doctor" | "patient" | "admin"
  userName?: string
  userEmail?: string
}

export function AppLayout({ children, userType, userName, userEmail }: AppLayoutProps) {
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false)

  return (
    <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
      <div className="flex h-screen bg-background">
        {isMobileSidebarOpen && (
          <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={() => setIsMobileSidebarOpen(false)} />
        )}

        <div
          className={`
          fixed lg:static inset-y-0 left-0 z-50 lg:z-auto
          transform ${isMobileSidebarOpen ? "translate-x-0" : "-translate-x-full"} 
          lg:translate-x-0 transition-transform duration-300 ease-in-out
        `}
        >
          <Sidebar userType={userType} onMobileClose={() => setIsMobileSidebarOpen(false)} />
        </div>

        <div className="flex-1 flex flex-col overflow-hidden lg:ml-0">
          <Navbar
            userType={userType}
            userName={userName}
            userEmail={userEmail}
            onMobileMenuClick={() => setIsMobileSidebarOpen(true)}
          />
          <main className="flex-1 overflow-auto p-3 sm:p-4 lg:p-6 w-full">
            <div className="w-full h-full">{children}</div>
          </main>
        </div>
      </div>
    </ThemeProvider>
  )
}
