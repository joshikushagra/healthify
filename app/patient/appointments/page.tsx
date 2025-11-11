import { AppLayout } from "@/components/layout/app-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Calendar, Clock, MapPin, Phone, Video, Plus, Filter } from "lucide-react"
import { Input } from "@/components/ui/input"

const appointments = [
  {
    id: 1,
    doctor: "Dr. Sarah Smith",
    specialty: "Cardiology",
    date: "2024-01-20",
    time: "10:00 AM",
    duration: "30 min",
    type: "Follow-up",
    location: "Room 205",
    status: "confirmed",
    mode: "in-person",
  },
  {
    id: 2,
    doctor: "Dr. Michael Johnson",
    specialty: "General Practice",
    date: "2024-01-25",
    time: "2:30 PM",
    duration: "45 min",
    type: "Annual Check-up",
    location: "Room 101",
    status: "confirmed",
    mode: "in-person",
  },
  {
    id: 3,
    doctor: "Dr. Emily Davis",
    specialty: "Dermatology",
    date: "2024-02-01",
    time: "11:15 AM",
    duration: "20 min",
    type: "Consultation",
    location: "Virtual",
    status: "pending",
    mode: "virtual",
  },
  {
    id: 4,
    doctor: "Dr. James Wilson",
    specialty: "Orthopedics",
    date: "2024-02-05",
    time: "3:00 PM",
    duration: "60 min",
    type: "Surgery Consultation",
    location: "Room 302",
    status: "confirmed",
    mode: "in-person",
  },
]

export default function PatientAppointmentsPage() {
  return (
    <AppLayout userType="patient" userName="John Doe" userEmail="john.doe@email.com">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground">My Appointments</h1>
            <p className="text-muted-foreground">Manage your upcoming and past appointments</p>
          </div>
          <Button className="gap-2">
            <Plus className="w-4 h-4" />
            Book Appointment
          </Button>
        </div>

        {/* Search and Filter */}
        <div className="flex gap-4">
          <div className="flex-1">
            <Input placeholder="Search appointments..." className="gap-2" />
          </div>
          <Button variant="outline" className="gap-2 bg-transparent">
            <Filter className="w-4 h-4" />
            Filter
          </Button>
        </div>

        {/* Appointments List */}
        <div className="space-y-4">
          {appointments.map((appointment) => (
            <Card key={appointment.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <Avatar className="w-12 h-12">
                      <AvatarImage src="/placeholder.svg" />
                      <AvatarFallback>
                        {appointment.doctor
                          .split(" ")
                          .map((n) => n[0])
                          .join("")}
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <h3 className="font-semibold text-lg">{appointment.doctor}</h3>
                      <p className="text-sm text-muted-foreground">{appointment.specialty}</p>
                      <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {appointment.date}
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {appointment.time} ({appointment.duration})
                        </div>
                        <div className="flex items-center gap-1">
                          {appointment.mode === "virtual" ? (
                            <Video className="w-4 h-4" />
                          ) : (
                            <MapPin className="w-4 h-4" />
                          )}
                          {appointment.location}
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="text-right space-y-2">
                    <Badge variant={appointment.status === "confirmed" ? "secondary" : "outline"} className="mb-2">
                      {appointment.status}
                    </Badge>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        Reschedule
                      </Button>
                      <Button variant="outline" size="sm">
                        Cancel
                      </Button>
                      {appointment.mode === "virtual" && (
                        <Button size="sm" className="gap-1">
                          <Video className="w-3 h-3" />
                          Join
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common appointment-related tasks</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button variant="outline" className="h-16 flex flex-col gap-2 bg-transparent">
                <Plus className="w-5 h-5" />
                <span className="text-sm">Book New Appointment</span>
              </Button>
              <Button variant="outline" className="h-16 flex flex-col gap-2 bg-transparent">
                <Calendar className="w-5 h-5" />
                <span className="text-sm">View Calendar</span>
              </Button>
              <Button variant="outline" className="h-16 flex flex-col gap-2 bg-transparent">
                <Phone className="w-5 h-5" />
                <span className="text-sm">Contact Support</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </AppLayout>
  )
}
