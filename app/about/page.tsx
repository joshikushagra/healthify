import { AppLayout } from "@/components/layout/app-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Stethoscope,
  Brain,
  Shield,
  Users,
  Award,
  Heart,
  Activity,
  MessageSquare,
  CheckCircle,
  Star,
} from "lucide-react"

const features = [
  {
    icon: Brain,
    title: "AI-Powered Diagnostics",
    description:
      "Advanced machine learning algorithms assist healthcare professionals in accurate diagnosis and treatment planning.",
  },
  {
    icon: Shield,
    title: "HIPAA Compliant",
    description: "Enterprise-grade security ensuring patient data privacy and compliance with healthcare regulations.",
  },
  {
    icon: Activity,
    title: "Real-time Monitoring",
    description: "Continuous health monitoring with instant alerts for critical changes in patient conditions.",
  },
  {
    icon: MessageSquare,
    title: "24/7 AI Assistant",
    description: "Round-the-clock medical guidance and support through our intelligent chatbot system.",
  },
]

const teamMembers = [
  {
    name: "Dr. Sarah Johnson",
    role: "Chief Medical Officer",
    specialty: "Internal Medicine",
    image: "/doctor-avatar.png",
    experience: "15+ years",
  },
  {
    name: "Dr. Michael Chen",
    role: "Head of Cardiology",
    specialty: "Cardiovascular Medicine",
    image: "/doctor-avatar.png",
    experience: "12+ years",
  },
  {
    name: "Dr. Emily Rodriguez",
    role: "Director of AI Research",
    specialty: "Medical Informatics",
    image: "/doctor-avatar.png",
    experience: "10+ years",
  },
  {
    name: "Dr. James Wilson",
    role: "Chief Technology Officer",
    specialty: "Healthcare Technology",
    image: "/doctor-avatar.png",
    experience: "8+ years",
  },
]

const stats = [
  { label: "Healthcare Providers", value: "10,000+", icon: Users },
  { label: "Patients Served", value: "500,000+", icon: Heart },
  { label: "AI Consultations", value: "1M+", icon: Brain },
  { label: "Accuracy Rate", value: "98.5%", icon: Award },
]

export default function AboutPage() {
  return (
    <AppLayout userType="patient" userName="Guest" userEmail="">
      <div className="space-y-8">
        {/* Hero Section */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-12 h-12 bg-primary rounded-lg flex items-center justify-center">
              <Stethoscope className="w-7 h-7 text-primary-foreground" />
            </div>
            <h1 className="text-4xl font-bold text-foreground">HEALTHIFY</h1>
          </div>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Revolutionizing healthcare through artificial intelligence, connecting patients and providers with
            cutting-edge medical technology for better health outcomes.
          </p>
          <div className="flex items-center justify-center gap-2">
            <Badge variant="secondary" className="gap-1">
              <Star className="w-3 h-3" />
              AI-Powered
            </Badge>
            <Badge variant="outline" className="gap-1">
              <Shield className="w-3 h-3" />
              HIPAA Compliant
            </Badge>
            <Badge variant="outline" className="gap-1">
              <CheckCircle className="w-3 h-3" />
              FDA Approved
            </Badge>
          </div>
        </div>

        {/* Mission Statement */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl text-center">Our Mission</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-lg text-muted-foreground text-center leading-relaxed">
              At HEALTHIFY, we believe that everyone deserves access to high-quality healthcare. Our mission is to
              democratize medical expertise through artificial intelligence, making advanced diagnostic tools and
              medical knowledge accessible to healthcare providers and patients worldwide. We're committed to improving
              health outcomes, reducing medical errors, and enhancing the overall healthcare experience through
              innovative technology.
            </p>
          </CardContent>
        </Card>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat) => {
            const Icon = stat.icon
            return (
              <Card key={stat.label} className="text-center">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-center mb-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                      <Icon className="w-6 h-6 text-primary" />
                    </div>
                  </div>
                  <div className="text-3xl font-bold text-foreground mb-2">{stat.value}</div>
                  <p className="text-sm text-muted-foreground">{stat.label}</p>
                </CardContent>
              </Card>
            )
          })}
        </div>

        {/* Features */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Key Features</CardTitle>
            <CardDescription>Advanced healthcare technology at your fingertips</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {features.map((feature) => {
                const Icon = feature.icon
                return (
                  <div key={feature.title} className="flex gap-4">
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Icon className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-foreground mb-2">{feature.title}</h3>
                      <p className="text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Team */}
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Our Medical Team</CardTitle>
            <CardDescription>Leading healthcare professionals and technology experts</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {teamMembers.map((member) => (
                <div key={member.name} className="text-center space-y-4">
                  <Avatar className="w-20 h-20 mx-auto">
                    <AvatarImage src={member.image || "/placeholder.svg"} />
                    <AvatarFallback className="text-lg">
                      {member.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>
                  <div>
                    <h3 className="font-semibold text-foreground">{member.name}</h3>
                    <p className="text-sm text-primary font-medium">{member.role}</p>
                    <p className="text-xs text-muted-foreground">{member.specialty}</p>
                    <Badge variant="outline" className="mt-2 text-xs">
                      {member.experience}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Call to Action */}
        <Card className="bg-primary/5 border-primary/20">
          <CardContent className="pt-6 text-center space-y-4">
            <h2 className="text-2xl font-bold text-foreground">Ready to Transform Healthcare?</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Join thousands of healthcare providers who trust HEALTHIFY to deliver better patient outcomes through
              AI-powered medical assistance.
            </p>
            <div className="flex gap-4 justify-center">
              <Button size="lg">Get Started Today</Button>
              <Button variant="outline" size="lg">
                Schedule Demo
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </AppLayout>
  )
}
