"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Eye, EyeOff, Mail, Lock, User, Stethoscope, Phone } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"

export default function SignupPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [userType, setUserType] = useState<"patient" | "doctor">("patient")
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    password: "",
    confirmPassword: "",
    specialization: "",
    licenseNumber: "",
    hospital: "",
    dateOfBirth: "",
    gender: "",
    address: "",
    emergencyContact: "",
    agreeToTerms: false,
    agreeToPrivacy: false,
  })
  const router = useRouter()

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault()
    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match")
      return
    }
    if (!formData.agreeToTerms || !formData.agreeToPrivacy) {
      alert("Please agree to the terms and privacy policy")
      return
    }
    if (userType === "doctor") {
      router.push("/doctor")
    } else {
      router.push("/patient")
    }
  }

  const handleSocialSignup = (provider: string) => {
    console.log(`Signup with ${provider}`)
  }

  const handleRoleChange = (value: string) => {
    setUserType(value as "patient" | "doctor")
    // Reset role-specific fields when switching
    setFormData({
      ...formData,
      specialization: "",
      licenseNumber: "",
      hospital: "",
      dateOfBirth: "",
      gender: "",
      emergencyContact: "",
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-peach-50 to-peach-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-peach-900 mb-2">Join HEALTHIFY</h1>
          <p className="text-peach-600">Create your account to get started</p>
        </div>

        <Card className="shadow-xl border-0">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl text-center text-peach-900">Sign Up</CardTitle>
            <CardDescription className="text-center text-peach-600">
              Choose your account type and create your profile
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* User Type Selection */}
            <div className="space-y-2">
              <Label className="text-peach-700 font-medium">Account Type</Label>
              <Tabs value={userType} onValueChange={handleRoleChange} className="w-full">
                <TabsList className="grid w-full grid-cols-2 bg-peach-100 p-1 rounded-lg">
                  <TabsTrigger
                    value="patient"
                    className="flex items-center gap-2 data-[state=active]:bg-peach-500 data-[state=active]:text-white data-[state=active]:shadow-sm transition-all duration-200 rounded-md"
                  >
                    <User className="h-4 w-4" />
                    Patient
                  </TabsTrigger>
                  <TabsTrigger
                    value="doctor"
                    className="flex items-center gap-2 data-[state=active]:bg-peach-500 data-[state=active]:text-white data-[state=active]:shadow-sm transition-all duration-200 rounded-md"
                  >
                    <Stethoscope className="h-4 w-4" />
                    Doctor
                  </TabsTrigger>
                </TabsList>
              </Tabs>
            </div>

            {/* Social Signup Options */}
            <div className="space-y-3">
              <Button
                variant="outline"
                className="w-full border-peach-200 hover:bg-peach-50 bg-transparent transition-colors"
                onClick={() => handleSocialSignup("google")}
              >
                <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                  <path
                    fill="#4285F4"
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  />
                  <path
                    fill="#EA4335"
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  />
                </svg>
                Sign up with Google
              </Button>

              <Button
                variant="outline"
                className="w-full border-peach-200 hover:bg-peach-50 bg-transparent transition-colors"
                onClick={() => handleSocialSignup("apple")}
              >
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z" />
                </svg>
                Sign up with Apple
              </Button>
            </div>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <Separator className="w-full bg-peach-200" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-2 text-peach-500">Or sign up with email</span>
              </div>
            </div>

            {/* Signup Form */}
            <form onSubmit={handleSignup} className="space-y-4">
              {/* Basic Information */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="firstName" className="text-peach-700">
                    First Name
                  </Label>
                  <Input
                    id="firstName"
                    type="text"
                    placeholder="Enter your first name"
                    value={formData.firstName}
                    onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                    className="border-peach-200 focus:border-peach-500"
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="lastName" className="text-peach-700">
                    Last Name
                  </Label>
                  <Input
                    id="lastName"
                    type="text"
                    placeholder="Enter your last name"
                    value={formData.lastName}
                    onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                    className="border-peach-200 focus:border-peach-500"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="email" className="text-peach-700">
                  Email
                </Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-peach-400" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="Enter your email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="pl-10 border-peach-200 focus:border-peach-500"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone" className="text-peach-700">
                  Phone Number
                </Label>
                <div className="relative">
                  <Phone className="absolute left-3 top-3 h-4 w-4 text-peach-400" />
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="Enter your phone number"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    className="pl-10 border-peach-200 focus:border-peach-500"
                    required
                  />
                </div>
              </div>

              {/* Doctor-specific fields */}
              {userType === "doctor" && (
                <div className="space-y-4 p-4 bg-peach-50 rounded-lg border border-peach-200">
                  <h3 className="text-lg font-semibold text-peach-800">Doctor Information</h3>
                  <div className="space-y-2">
                    <Label htmlFor="specialization" className="text-peach-700">
                      Specialization
                    </Label>
                    <Select
                      value={formData.specialization}
                      onValueChange={(value) => setFormData({ ...formData, specialization: value })}
                    >
                      <SelectTrigger className="border-peach-200 focus:border-peach-500">
                        <SelectValue placeholder="Select your specialization" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="cardiology">Cardiology</SelectItem>
                        <SelectItem value="dermatology">Dermatology</SelectItem>
                        <SelectItem value="endocrinology">Endocrinology</SelectItem>
                        <SelectItem value="gastroenterology">Gastroenterology</SelectItem>
                        <SelectItem value="neurology">Neurology</SelectItem>
                        <SelectItem value="oncology">Oncology</SelectItem>
                        <SelectItem value="orthopedics">Orthopedics</SelectItem>
                        <SelectItem value="pediatrics">Pediatrics</SelectItem>
                        <SelectItem value="psychiatry">Psychiatry</SelectItem>
                        <SelectItem value="general">General Practice</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="licenseNumber" className="text-peach-700">
                        License Number
                      </Label>
                      <Input
                        id="licenseNumber"
                        type="text"
                        placeholder="Enter your license number"
                        value={formData.licenseNumber}
                        onChange={(e) => setFormData({ ...formData, licenseNumber: e.target.value })}
                        className="border-peach-200 focus:border-peach-500"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="hospital" className="text-peach-700">
                        Hospital/Clinic
                      </Label>
                      <Input
                        id="hospital"
                        type="text"
                        placeholder="Enter your workplace"
                        value={formData.hospital}
                        onChange={(e) => setFormData({ ...formData, hospital: e.target.value })}
                        className="border-peach-200 focus:border-peach-500"
                        required
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Patient-specific fields */}
              {userType === "patient" && (
                <div className="space-y-4 p-4 bg-peach-50 rounded-lg border border-peach-200">
                  <h3 className="text-lg font-semibold text-peach-800">Patient Information</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="dateOfBirth" className="text-peach-700">
                        Date of Birth
                      </Label>
                      <Input
                        id="dateOfBirth"
                        type="date"
                        value={formData.dateOfBirth}
                        onChange={(e) => setFormData({ ...formData, dateOfBirth: e.target.value })}
                        className="border-peach-200 focus:border-peach-500"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="gender" className="text-peach-700">
                        Gender
                      </Label>
                      <Select
                        value={formData.gender}
                        onValueChange={(value) => setFormData({ ...formData, gender: value })}
                      >
                        <SelectTrigger className="border-peach-200 focus:border-peach-500">
                          <SelectValue placeholder="Select gender" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="male">Male</SelectItem>
                          <SelectItem value="female">Female</SelectItem>
                          <SelectItem value="other">Other</SelectItem>
                          <SelectItem value="prefer-not-to-say">Prefer not to say</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="emergencyContact" className="text-peach-700">
                      Emergency Contact
                    </Label>
                    <Input
                      id="emergencyContact"
                      type="tel"
                      placeholder="Emergency contact phone number"
                      value={formData.emergencyContact}
                      onChange={(e) => setFormData({ ...formData, emergencyContact: e.target.value })}
                      className="border-peach-200 focus:border-peach-500"
                      required
                    />
                  </div>
                </div>
              )}

              {/* Password Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-peach-700">
                    Password
                  </Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-peach-400" />
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Create a password"
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      className="pl-10 pr-10 border-peach-200 focus:border-peach-500"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-3 text-peach-400 hover:text-peach-600"
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword" className="text-peach-700">
                    Confirm Password
                  </Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-peach-400" />
                    <Input
                      id="confirmPassword"
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="Confirm your password"
                      value={formData.confirmPassword}
                      onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                      className="pl-10 pr-10 border-peach-200 focus:border-peach-500"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-3 text-peach-400 hover:text-peach-600"
                    >
                      {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                </div>
              </div>

              {/* Terms and Privacy */}
              <div className="space-y-3">
                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="terms"
                    checked={formData.agreeToTerms}
                    onCheckedChange={(checked) => setFormData({ ...formData, agreeToTerms: checked as boolean })}
                    className="border-peach-300 data-[state=checked]:bg-peach-500"
                  />
                  <Label htmlFor="terms" className="text-sm text-peach-600">
                    I agree to the{" "}
                    <Link href="/terms" className="text-peach-700 hover:text-peach-900 underline">
                      Terms of Service
                    </Link>
                  </Label>
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="privacy"
                    checked={formData.agreeToPrivacy}
                    onCheckedChange={(checked) => setFormData({ ...formData, agreeToPrivacy: checked as boolean })}
                    className="border-peach-300 data-[state=checked]:bg-peach-500"
                  />
                  <Label htmlFor="privacy" className="text-sm text-peach-600">
                    I agree to the{" "}
                    <Link href="/privacy" className="text-peach-700 hover:text-peach-900 underline">
                      Privacy Policy
                    </Link>
                  </Label>
                </div>
              </div>

              <Button type="submit" className="w-full bg-peach-500 hover:bg-peach-600 text-white">
                Create {userType === "doctor" ? "Doctor" : "Patient"} Account
              </Button>
            </form>

            <div className="text-center">
              <p className="text-sm text-peach-600">
                Already have an account?{" "}
                <Link href="/auth/login" className="text-peach-700 hover:text-peach-900 font-medium">
                  Sign in
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
