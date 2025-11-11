import { AppLayout } from "@/components/layout/app-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Users, Calendar, Activity, TrendingUp, Clock, AlertTriangle, MessageSquare, FileText } from "lucide-react"
import Link from "next/link"

const recentPatients = [
  {
    id: 1,
    name: "Sarah Johnson",
    age: 34,
    condition: "Hypertension",
    lastVisit: "2024-01-15",
    status: "stable",
    avatar: "/patient1.png",
  },
  {
    id: 2,
    name: "Michael Chen",
    age: 45,
    condition: "Diabetes Type 2",
    lastVisit: "2024-01-14",
    status: "monitoring",
    avatar: "/patient2.png",
  },
  {
    id: 3,
    name: "Emily Davis",
    age: 28,
    condition: "Asthma",
    lastVisit: "2024-01-13",
    status: "improved",
    avatar: "/patient3.png",
  },
  {
    id: 4,
    name: "Robert Wilson",
    age: 52,
    condition: "Cardiac Arrhythmia",
    lastVisit: "2024-01-12",
    status: "critical",
    avatar: "/patient4.png",
  },
]

const upcomingAppointments = [
  {
    id: 1,
    patient: "Jennifer Martinez",
    time: "09:00 AM",
    type: "Follow-up",
    duration: "30 min",
  },
  {
    id: 2,
    patient: "David Thompson",
    time: "10:30 AM",
    type: "Consultation",
    duration: "45 min",
  },
  {
    id: 3,
    patient: "Lisa Anderson",
    time: "02:00 PM",
    type: "Check-up",
    duration: "30 min",
  },
  {
    id: 4,
    patient: "James Brown",
    time: "03:30 PM",
    type: "Emergency",
    duration: "60 min",
  },
]

const vitalAlerts = [
  {
    id: 1,
    patient: "Robert Wilson",
    alert: "High Blood Pressure",
    value: "180/110 mmHg",
    severity: "critical",
    time: "2 hours ago",
  },
  {
    id: 2,
    patient: "Michael Chen",
    alert: "Blood Sugar Spike",
    value: "280 mg/dL",
    severity: "warning",
    time: "4 hours ago",
  },
  {
    id: 3,
    patient: "Sarah Johnson",
    alert: "Heart Rate Elevated",
    value: "105 BPM",
    severity: "moderate",
    time: "6 hours ago",
  },
]

export default function DoctorDashboard() {
  return (
    <AppLayout userType="doctor" userName="Dr. Sarah Smith" userEmail="dr.smith@medai.com">
      <div className="max-w-7xl mx-auto space-y-4 sm:space-y-6">
        {/* Welcome Section */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground">Good morning, Dr. Smith</h1>
            <p className="text-muted-foreground">Here's what's happening with your patients today</p>
          </div>
          <div className="flex flex-col sm:flex-row gap-2 sm:gap-3">
            <Link href="/chat">
              <Button variant="outline" className="gap-2 bg-transparent w-full sm:w-auto">
                <MessageSquare className="w-4 h-4" />
                <span className="hidden sm:inline">AI Assistant</span>
                <span className="sm:hidden">AI</span>
              </Button>
            </Link>
            <Link href="/patient/appointments">
              <Button className="gap-2 w-full sm:w-auto">
                <Calendar className="w-4 h-4" />
                <span className="hidden sm:inline">Schedule Appointment</span>
                <span className="sm:hidden">Schedule</span>
              </Button>
            </Link>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium">Total Patients</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-xl sm:text-2xl font-bold">247</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-green-600">+12%</span> from last month
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium">Today's Appointments</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-xl sm:text-2xl font-bold">8</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-blue-600">2 emergency</span> slots available
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium">Critical Alerts</CardTitle>
              <AlertTriangle className="h-4 w-4 text-destructive" />
            </CardHeader>
            <CardContent>
              <div className="text-xl sm:text-2xl font-bold text-destructive">3</div>
              <p className="text-xs text-muted-foreground">Require immediate attention</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs sm:text-sm font-medium">Patient Satisfaction</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-xl sm:text-2xl font-bold">94%</div>
              <p className="text-xs text-muted-foreground">
                <span className="text-green-600">+2%</span> from last week
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
          {/* Recent Patients */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="w-5 h-5" />
                Recent Patients
              </CardTitle>
              <CardDescription>Latest patient interactions and status updates</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentPatients.map((patient) => (
                  <div
                    key={patient.id}
                    className="flex items-center justify-between p-3 sm:p-4 border border-border rounded-lg hover:bg-muted/50 transition-colors"
                  >
                    <div className="flex items-center gap-3 sm:gap-4 min-w-0 flex-1">
                      <Avatar className="h-8 w-8 sm:h-10 sm:w-10 flex-shrink-0">
                        <AvatarImage src={patient.avatar || "/placeholder.svg"} />
                        <AvatarFallback>
                          {patient.name
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                        </AvatarFallback>
                      </Avatar>
                      <div className="min-w-0 flex-1">
                        <h4 className="font-semibold text-sm sm:text-base truncate">{patient.name}</h4>
                        <p className="text-xs sm:text-sm text-muted-foreground">
                          Age {patient.age} • {patient.condition}
                        </p>
                        <p className="text-xs text-muted-foreground hidden sm:block">Last visit: {patient.lastVisit}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
                      <Badge
                        variant={
                          patient.status === "critical"
                            ? "destructive"
                            : patient.status === "stable"
                              ? "default"
                              : patient.status === "improved"
                                ? "secondary"
                                : "outline"
                        }
                        className="text-xs"
                      >
                        {patient.status}
                      </Badge>
                      <Link href="/patient/records">
                        <Button variant="ghost" size="sm" className="hidden sm:flex">
                          <FileText className="w-4 h-4" />
                        </Button>
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Today's Schedule */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="w-5 h-5" />
                Today's Schedule
              </CardTitle>
              <CardDescription>Upcoming appointments</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {upcomingAppointments.map((appointment) => (
                  <div
                    key={appointment.id}
                    className="flex items-center justify-between p-3 border border-border rounded-lg"
                  >
                    <div>
                      <h4 className="font-medium text-sm">{appointment.patient}</h4>
                      <p className="text-xs text-muted-foreground">{appointment.type}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium">{appointment.time}</p>
                      <p className="text-xs text-muted-foreground">{appointment.duration}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-4 sm:gap-6">
          {/* Vital Alerts */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-destructive" />
                Critical Vital Alerts
              </CardTitle>
              <CardDescription>Patients requiring immediate attention</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {vitalAlerts.map((alert) => (
                  <div key={alert.id} className="flex items-center justify-between p-4 border border-border rounded-lg">
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-3 h-3 rounded-full ${
                          alert.severity === "critical"
                            ? "bg-destructive"
                            : alert.severity === "warning"
                              ? "bg-yellow-500"
                              : "bg-orange-500"
                        }`}
                      />
                      <div>
                        <h4 className="font-medium text-sm">{alert.patient}</h4>
                        <p className="text-sm text-muted-foreground">{alert.alert}</p>
                        <p className="text-xs text-muted-foreground">{alert.time}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-sm">{alert.value}</p>
                      <Link href="/patient/records">
                        <Button variant="outline" size="sm" className="mt-1 bg-transparent">
                          Review
                        </Button>
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5" />
                Quick Actions
              </CardTitle>
              <CardDescription>Common tasks and tools</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-4">
                <Link href="/chat">
                  <Button variant="outline" className="h-20 flex flex-col gap-2 bg-transparent w-full">
                    <MessageSquare className="w-6 h-6" />
                    <span className="text-sm">AI Consult</span>
                  </Button>
                </Link>
                <Link href="/patient/records">
                  <Button variant="outline" className="h-20 flex flex-col gap-2 bg-transparent w-full">
                    <FileText className="w-6 h-6" />
                    <span className="text-sm">New Report</span>
                  </Button>
                </Link>
                <Link href="/patient/appointments">
                  <Button variant="outline" className="h-20 flex flex-col gap-2 bg-transparent w-full">
                    <Calendar className="w-6 h-6" />
                    <span className="text-sm">Schedule</span>
                  </Button>
                </Link>
                <Link href="/patient">
                  <Button variant="outline" className="h-20 flex flex-col gap-2 bg-transparent w-full">
                    <Users className="w-6 h-6" />
                    <span className="text-sm">Patient List</span>
                  </Button>
                </Link>
              </div>

              <div className="mt-6 p-4 bg-muted/50 rounded-lg">
                <h4 className="font-medium text-sm mb-2">Today's Progress</h4>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Appointments Completed</span>
                    <span>5/8</span>
                  </div>
                  <Progress value={62.5} className="h-2" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}
