"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Mail, ArrowLeft } from "lucide-react"
import Link from "next/link"

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("")
  const [isSubmitted, setIsSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-peach-50 to-peach-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-peach-900 mb-2">Reset Password</h1>
          <p className="text-peach-600">We'll send you a link to reset your password</p>
        </div>

        <Card className="shadow-xl border-0">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl text-center text-peach-900">Forgot Password</CardTitle>
            <CardDescription className="text-center text-peach-600">
              {isSubmitted
                ? "Check your email for reset instructions"
                : "Enter your email address to reset your password"}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {!isSubmitted ? (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-peach-700">
                    Email Address
                  </Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-peach-400" />
                    <Input
                      id="email"
                      type="email"
                      placeholder="Enter your email address"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="pl-10 border-peach-200 focus:border-peach-500"
                      required
                    />
                  </div>
                </div>

                <Button type="submit" className="w-full bg-peach-500 hover:bg-peach-600 text-white">
                  Send Reset Link
                </Button>
              </form>
            ) : (
              <div className="text-center space-y-4">
                <div className="w-16 h-16 bg-peach-100 rounded-full flex items-center justify-center mx-auto">
                  <Mail className="h-8 w-8 text-peach-500" />
                </div>
                <p className="text-peach-600">
                  We've sent a password reset link to <strong>{email}</strong>
                </p>
                <p className="text-sm text-peach-500">Didn't receive the email? Check your spam folder or try again.</p>
                <Button
                  onClick={() => setIsSubmitted(false)}
                  variant="outline"
                  className="border-peach-200 hover:bg-peach-50"
                >
                  Try Again
                </Button>
              </div>
            )}

            <div className="text-center">
              <Link href="/auth/login" className="inline-flex items-center text-sm text-peach-600 hover:text-peach-800">
                <ArrowLeft className="h-4 w-4 mr-1" />
                Back to Sign In
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
