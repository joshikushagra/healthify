import { AppLayout } from "@/components/layout/app-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { FileText, Download, Eye, Filter, Calendar, User, Activity, Heart, TestTube } from "lucide-react"

const medicalRecords = [
  {
    id: 1,
    title: "Annual Physical Examination",
    doctor: "Dr. Michael Johnson",
    date: "2024-01-15",
    type: "Examination",
    category: "General",
    status: "completed",
    fileSize: "2.4 MB",
  },
  {
    id: 2,
    title: "Cardiology Consultation Report",
    doctor: "Dr. Sarah Smith",
    date: "2024-01-10",
    type: "Consultation",
    category: "Cardiology",
    status: "completed",
    fileSize: "1.8 MB",
  },
  {
    id: 3,
    title: "Blood Test Results - Complete Panel",
    doctor: "Dr. Sarah Smith",
    date: "2024-01-08",
    type: "Lab Results",
    category: "Laboratory",
    status: "completed",
    fileSize: "856 KB",
  },
  {
    id: 4,
    title: "Chest X-Ray Report",
    doctor: "Dr. Michael Johnson",
    date: "2024-01-05",
    type: "Imaging",
    category: "Radiology",
    status: "completed",
    fileSize: "3.2 MB",
  },
  {
    id: 5,
    title: "Prescription - Lisinopril",
    doctor: "Dr. Sarah Smith",
    date: "2024-01-03",
    type: "Prescription",
    category: "Medication",
    status: "active",
    fileSize: "124 KB",
  },
]

const recordCategories = [
  { name: "All Records", count: 15, icon: FileText },
  { name: "Lab Results", count: 5, icon: TestTube },
  { name: "Imaging", count: 3, icon: Activity },
  { name: "Prescriptions", count: 4, icon: Heart },
  { name: "Consultations", count: 3, icon: User },
]

export default function PatientRecordsPage() {
  return (
    <AppLayout userType="patient" userName="John Doe" userEmail="john.doe@email.com">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Medical Records</h1>
            <p className="text-muted-foreground">Access and manage your medical documents</p>
          </div>
          <Button variant="outline" className="gap-2 bg-transparent">
            <Download className="w-4 h-4" />
            Export All
          </Button>
        </div>

        <div className="grid lg:grid-cols-4 gap-6">
          {/* Categories Sidebar */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Categories</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {recordCategories.map((category) => {
                  const Icon = category.icon
                  return (
                    <Button key={category.name} variant="ghost" className="w-full justify-between">
                      <div className="flex items-center gap-2">
                        <Icon className="w-4 h-4" />
                        {category.name}
                      </div>
                      <Badge variant="secondary" className="text-xs">
                        {category.count}
                      </Badge>
                    </Button>
                  )
                })}
              </CardContent>
            </Card>
          </div>

          {/* Records List */}
          <div className="lg:col-span-3 space-y-6">
            {/* Search and Filter */}
            <div className="flex gap-4">
              <div className="flex-1">
                <Input placeholder="Search medical records..." className="gap-2" />
              </div>
              <Button variant="outline" className="gap-2 bg-transparent">
                <Filter className="w-4 h-4" />
                Filter
              </Button>
              <Button variant="outline" className="gap-2 bg-transparent">
                <Calendar className="w-4 h-4" />
                Date Range
              </Button>
            </div>

            {/* Records */}
            <div className="space-y-4">
              {medicalRecords.map((record) => (
                <Card key={record.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-start gap-4">
                        <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                          <FileText className="w-6 h-6 text-primary" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-lg mb-1">{record.title}</h3>
                          <div className="space-y-1 text-sm text-muted-foreground">
                            <p>By {record.doctor}</p>
                            <p>
                              {record.date} • {record.fileSize}
                            </p>
                            <div className="flex items-center gap-2 mt-2">
                              <Badge variant="outline" className="text-xs">
                                {record.type}
                              </Badge>
                              <Badge variant="secondary" className="text-xs">
                                {record.category}
                              </Badge>
                              <Badge variant={record.status === "active" ? "default" : "secondary"} className="text-xs">
                                {record.status}
                              </Badge>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <Button variant="outline" size="sm" className="gap-1 bg-transparent">
                          <Eye className="w-3 h-3" />
                          View
                        </Button>
                        <Button variant="outline" size="sm" className="gap-1 bg-transparent">
                          <Download className="w-3 h-3" />
                          Download
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Summary Stats */}
            <Card>
              <CardHeader>
                <CardTitle>Records Summary</CardTitle>
                <CardDescription>Overview of your medical records</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="text-center p-4 border border-border rounded-lg">
                    <div className="text-2xl font-bold text-primary">15</div>
                    <p className="text-sm text-muted-foreground">Total Records</p>
                  </div>
                  <div className="text-center p-4 border border-border rounded-lg">
                    <div className="text-2xl font-bold text-primary">5</div>
                    <p className="text-sm text-muted-foreground">This Month</p>
                  </div>
                  <div className="text-center p-4 border border-border rounded-lg">
                    <div className="text-2xl font-bold text-primary">3</div>
                    <p className="text-sm text-muted-foreground">Pending Review</p>
                  </div>
                  <div className="text-center p-4 border border-border rounded-lg">
                    <div className="text-2xl font-bold text-primary">12.4</div>
                    <p className="text-sm text-muted-foreground">Total Size (MB)</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
