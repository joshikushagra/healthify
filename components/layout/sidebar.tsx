"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Home, MessageSquare, Stethoscope, Users, Settings, Menu, X, Activity, Calendar, FileText } from "lucide-react"

interface SidebarProps {
  userType: "doctor" | "patient" | "admin"
  onMobileClose?: () => void
}

export function Sidebar({ userType, onMobileClose }: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false)
  const pathname = usePathname()

  const getNavItems = () => {
    const commonItems = [
      { href: "/", icon: Home, label: "Home" },
      { href: "/chat", icon: MessageSquare, label: "AI Assistant" },
      { href: "/about", icon: FileText, label: "About" },
      { href: "/contact", icon: MessageSquare, label: "Contact" },
    ]

    if (userType === "doctor") {
      return [
        ...commonItems,
        { href: "/doctor", icon: Stethoscope, label: "Dashboard" },
        { href: "/doctor/patients", icon: Users, label: "Patients" },
        { href: "/doctor/appointments", icon: Calendar, label: "Appointments" },
        { href: "/doctor/reports", icon: FileText, label: "Reports" },
        { href: "/settings", icon: Settings, label: "Settings" },
      ]
    }

    if (userType === "patient") {
      return [
        ...commonItems,
        { href: "/patient", icon: Activity, label: "Dashboard" },
        { href: "/patient/appointments", icon: Calendar, label: "Appointments" },
        { href: "/patient/records", icon: FileText, label: "Medical Records" },
        { href: "/settings", icon: Settings, label: "Settings" },
      ]
    }

    return commonItems
  }

  const navItems = getNavItems()

  const handleLinkClick = () => {
    if (onMobileClose) {
      onMobileClose()
    }
  }

  return (
    <div
      className={cn(
        "flex flex-col h-full bg-sidebar border-r border-sidebar-border transition-all duration-300",
        "w-64 lg:w-64",
        isCollapsed && "lg:w-16",
      )}
    >
      <div className="flex items-center justify-between p-4 border-b border-sidebar-border">
        {!isCollapsed && (
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Stethoscope className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="font-semibold text-sidebar-foreground">HEALTHIFY</span>
          </div>
        )}
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="hidden lg:flex text-sidebar-foreground hover:bg-sidebar-accent"
          >
            {isCollapsed ? <Menu className="w-4 h-4" /> : <X className="w-4 h-4" />}
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={onMobileClose}
            className="lg:hidden text-sidebar-foreground hover:bg-sidebar-accent"
          >
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <ScrollArea className="flex-1 px-3 py-4">
        <nav className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href

            return (
              <Link key={item.href} href={item.href} onClick={handleLinkClick}>
                <Button
                  variant={isActive ? "default" : "ghost"}
                  className={cn(
                    "w-full justify-start gap-3 text-sidebar-foreground hover:bg-sidebar-accent",
                    isActive && "bg-sidebar-primary text-sidebar-primary-foreground hover:bg-sidebar-primary/90",
                    isCollapsed && "lg:px-2",
                  )}
                >
                  <Icon className="w-5 h-5 flex-shrink-0" />
                  {(!isCollapsed || window.innerWidth < 1024) && <span>{item.label}</span>}
                </Button>
              </Link>
            )
          })}
        </nav>
      </ScrollArea>
    </div>
  )
}
