import { AppLayout } from "@/components/layout/app-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Calendar,
  Activity,
  Heart,
  Thermometer,
  Weight,
  Pill,
  FileText,
  MessageSquare,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  User,
  Ruler,
  Droplets,
} from "lucide-react"
import Link from "next/link"

const basicHealthInfo = [
  {
    id: 1,
    name: "Blood Group",
    value: "O+",
    icon: Droplets,
    category: "Basic Info",
  },
  {
    id: 2,
    name: "Height",
    value: "5'8\"",
    unit: "ft",
    icon: Ruler,
    category: "Physical",
  },
  {
    id: 3,
    name: "Weight",
    value: "165",
    unit: "lbs",
    icon: Weight,
    category: "Physical",
    trend: "stable",
  },
  {
    id: 4,
    name: "Age",
    value: "32",
    unit: "years",
    icon: User,
    category: "Basic Info",
  },
]

const vitalSigns = [
  {
    id: 1,
    name: "Blood Pressure",
    value: "120/80",
    unit: "mmHg",
    status: "normal",
    icon: Heart,
    trend: "stable",
    lastUpdated: "2 hours ago",
  },
  {
    id: 2,
    name: "Heart Rate",
    value: "72",
    unit: "BPM",
    status: "normal",
    icon: Activity,
    trend: "stable",
    lastUpdated: "2 hours ago",
  },
  {
    id: 3,
    name: "Temperature",
    value: "98.6",
    unit: "°F",
    status: "normal",
    icon: Thermometer,
    trend: "stable",
    lastUpdated: "4 hours ago",
  },
  {
    id: 4,
    name: "BMI",
    value: "24.2",
    unit: "kg/m²",
    status: "normal",
    icon: Activity,
    trend: "stable",
    lastUpdated: "1 week ago",
  },
]

const upcomingAppointments = [
  {
    id: 1,
    doctor: "Dr. Sarah Smith",
    specialty: "Cardiology",
    date: "2024-01-20",
    time: "10:00 AM",
    type: "Follow-up",
    location: "Room 205",
  },
  {
    id: 2,
    doctor: "Dr. Michael Johnson",
    specialty: "General Practice",
    date: "2024-01-25",
    time: "2:30 PM",
    type: "Annual Check-up",
    location: "Room 101",
  },
  {
    id: 3,
    doctor: "Dr. Emily Davis",
    specialty: "Dermatology",
    date: "2024-02-01",
    time: "11:15 AM",
    type: "Consultation",
    location: "Room 308",
  },
]

const medications = [
  {
    id: 1,
    name: "Lisinopril",
    dosage: "10mg",
    frequency: "Once daily",
    timeToTake: "Morning",
    remaining: 25,
    total: 30,
    status: "active",
  },
  {
    id: 2,
    name: "Metformin",
    dosage: "500mg",
    frequency: "Twice daily",
    timeToTake: "With meals",
    remaining: 45,
    total: 60,
    status: "active",
  },
  {
    id: 3,
    name: "Vitamin D3",
    dosage: "1000 IU",
    frequency: "Once daily",
    timeToTake: "Morning",
    remaining: 8,
    total: 30,
    status: "low",
  },
]

const recentResults = [
  {
    id: 1,
    test: "Complete Blood Count",
    date: "2024-01-10",
    status: "normal",
    doctor: "Dr. Sarah Smith",
  },
  {
    id: 2,
    test: "Lipid Panel",
    date: "2024-01-08",
    status: "review",
    doctor: "Dr. Sarah Smith",
  },
  {
    id: 3,
    test: "HbA1c",
    date: "2024-01-05",
    status: "normal",
    doctor: "Dr. Michael Johnson",
  },
]

export default function PatientDashboard() {
  return (
    <AppLayout userType="patient" userName="John Doe" userEmail="john.doe@email.com">
      <div className="space-y-6 lg:space-y-8 p-4 lg:p-6 max-w-7xl mx-auto">
        {/* Welcome Section */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 lg:gap-6">
          <div className="flex-1">
            <h1 className="text-2xl lg:text-4xl font-bold text-foreground mb-2">Welcome back, John</h1>
            <p className="text-base lg:text-lg text-muted-foreground">Here's your health overview for today</p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3 lg:gap-4 min-w-fit">
            <Link href="/chat">
              <Button variant="outline" className="gap-2 bg-transparent w-full sm:w-auto">
                <MessageSquare className="w-4 h-4" />
                <span className="hidden sm:inline">Ask AI Assistant</span>
                <span className="sm:hidden">AI Assistant</span>
              </Button>
            </Link>
            <Link href="/patient/appointments">
              <Button className="gap-2 w-full sm:w-auto">
                <Calendar className="w-4 h-4" />
                <span className="hidden sm:inline">Book Appointment</span>
                <span className="sm:hidden">Book Appointment</span>
              </Button>
            </Link>
          </div>
        </div>

        {/* Basic Health Information Section */}
        <Card className="shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center gap-2 text-xl">
              <User className="w-6 h-6" />
              Basic Health Information
            </CardTitle>
            <CardDescription className="text-base">Your essential health details</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 lg:gap-6">
              {basicHealthInfo.map((info) => {
                const Icon = info.icon
                return (
                  <div
                    key={info.id}
                    className="flex items-center gap-3 lg:gap-4 p-4 lg:p-6 border border-border rounded-xl hover:shadow-md transition-all duration-200"
                  >
                    <div className="p-3 bg-primary/10 rounded-xl flex-shrink-0">
                      <Icon className="h-6 w-6 lg:h-7 lg:w-7 text-primary" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <p className="text-sm lg:text-base font-medium text-muted-foreground mb-1">{info.name}</p>
                      <p className="text-xl lg:text-2xl font-bold text-foreground">
                        {info.value}{" "}
                        {info.unit && (
                          <span className="text-sm lg:text-base font-normal text-muted-foreground">{info.unit}</span>
                        )}
                      </p>
                      <p className="text-xs lg:text-sm text-muted-foreground mt-1">{info.category}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Health Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 lg:gap-6">
          {vitalSigns.map((vital) => {
            const Icon = vital.icon
            return (
              <Card key={vital.id} className="shadow-sm hover:shadow-md transition-all duration-200">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
                  <CardTitle className="text-sm lg:text-base font-medium">{vital.name}</CardTitle>
                  <Icon className="h-5 w-5 lg:h-6 lg:w-6 text-muted-foreground" />
                </CardHeader>
                <CardContent className="pt-0">
                  <div className="text-2xl lg:text-3xl font-bold mb-2">
                    {vital.value}{" "}
                    <span className="text-sm lg:text-base font-normal text-muted-foreground">{vital.unit}</span>
                  </div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <Badge
                      variant={
                        vital.status === "normal" ? "secondary" : vital.status === "warning" ? "destructive" : "outline"
                      }
                      className="text-xs"
                    >
                      {vital.status}
                    </Badge>
                    <p className="text-xs text-muted-foreground">{vital.lastUpdated}</p>
                  </div>
                </CardContent>
              </Card>
            )
          })}
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 lg:gap-8">
          {/* Upcoming Appointments */}
          <Card className="xl:col-span-2 shadow-sm">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2 text-xl">
                <Calendar className="w-6 h-6" />
                Upcoming Appointments
              </CardTitle>
              <CardDescription className="text-base">Your scheduled medical appointments</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 lg:space-y-6">
                {upcomingAppointments.map((appointment) => (
                  <div
                    key={appointment.id}
                    className="flex flex-col sm:flex-row sm:items-center justify-between p-4 lg:p-6 border border-border rounded-xl hover:bg-muted/50 transition-colors gap-4"
                  >
                    <div className="flex items-center gap-4">
                      <Avatar className="h-12 w-12 lg:h-14 lg:w-14">
                        <AvatarImage src="/placeholder.svg" />
                        <AvatarFallback className="text-lg">
                          {appointment.doctor
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1">
                        <h4 className="font-semibold text-base lg:text-lg">{appointment.doctor}</h4>
                        <p className="text-sm lg:text-base text-muted-foreground">
                          {appointment.specialty} • {appointment.type}
                        </p>
                        <p className="text-xs lg:text-sm text-muted-foreground">{appointment.location}</p>
                      </div>
                    </div>
                    <div className="text-left sm:text-right flex-shrink-0">
                      <p className="font-medium text-base lg:text-lg">{appointment.date}</p>
                      <p className="text-sm lg:text-base text-muted-foreground mb-3">{appointment.time}</p>
                      <Button variant="outline" size="sm" className="bg-transparent">
                        Reschedule
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Medications */}
          <Card className="shadow-sm">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2 text-xl">
                <Pill className="w-6 h-6" />
                Current Medications
              </CardTitle>
              <CardDescription className="text-base">Your active prescriptions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 lg:space-y-6">
                {medications.map((medication) => (
                  <div key={medication.id} className="p-4 lg:p-5 border border-border rounded-xl">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-medium text-base lg:text-lg">{medication.name}</h4>
                      <Badge variant={medication.status === "low" ? "destructive" : "secondary"} className="text-xs">
                        {medication.status === "low" ? "Refill Soon" : "Active"}
                      </Badge>
                    </div>
                    <p className="text-sm lg:text-base text-muted-foreground mb-3">
                      {medication.dosage} • {medication.frequency} • {medication.timeToTake}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">
                        {medication.remaining}/{medication.total} pills left
                      </span>
                      <Progress value={(medication.remaining / medication.total) * 100} className="w-20 h-3" />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 lg:gap-8">
          {/* Recent Test Results */}
          <Card className="shadow-sm">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2 text-xl">
                <FileText className="w-6 h-6" />
                Recent Test Results
              </CardTitle>
              <CardDescription className="text-base">Latest lab results and reports</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 lg:space-y-6">
                {recentResults.map((result) => (
                  <div
                    key={result.id}
                    className="flex items-center justify-between p-4 lg:p-6 border border-border rounded-xl"
                  >
                    <div className="flex items-center gap-4">
                      {result.status === "normal" ? (
                        <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0" />
                      ) : (
                        <AlertCircle className="w-6 h-6 text-yellow-500 flex-shrink-0" />
                      )}
                      <div className="flex-1">
                        <h4 className="font-medium text-base lg:text-lg">{result.test}</h4>
                        <p className="text-sm text-muted-foreground">by {result.doctor}</p>
                        <p className="text-sm text-muted-foreground">{result.date}</p>
                      </div>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <Badge variant={result.status === "normal" ? "secondary" : "outline"} className="mb-3">
                        {result.status}
                      </Badge>
                      <br />
                      <Button variant="outline" size="sm">
                        View Report
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Health Goals */}
          <Card className="shadow-sm">
            <CardHeader className="pb-4">
              <CardTitle className="flex items-center gap-2 text-xl">
                <TrendingUp className="w-6 h-6" />
                Health Goals
              </CardTitle>
              <CardDescription className="text-base">Track your wellness journey</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6 lg:space-y-8">
                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-base font-medium">Daily Water Intake</span>
                    <span className="text-sm text-muted-foreground">6 / 8 glasses</span>
                  </div>
                  <Progress value={75} className="h-3" />
                </div>

                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-base font-medium">Exercise Minutes</span>
                    <span className="text-sm text-muted-foreground">25 / 30 min</span>
                  </div>
                  <Progress value={83.33} className="h-3" />
                </div>

                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-base font-medium">Sleep Hours</span>
                    <span className="text-sm text-muted-foreground">7.5 / 8 hours</span>
                  </div>
                  <Progress value={93.75} className="h-3" />
                </div>

                <div className="pt-6 border-t border-border">
                  <h4 className="font-medium text-base lg:text-lg mb-4">Quick Actions</h4>
                  <div className="grid grid-cols-2 gap-3">
                    <Button variant="outline" size="sm" className="h-16 flex flex-col gap-2 bg-transparent">
                      <Activity className="w-5 h-5" />
                      <span className="text-sm">Log Vitals</span>
                    </Button>
                    <Link href="/chat">
                      <Button variant="outline" size="sm" className="h-16 flex flex-col gap-2 bg-transparent w-full">
                        <MessageSquare className="w-5 h-5" />
                        <span className="text-sm">Ask AI</span>
                      </Button>
                    </Link>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}
