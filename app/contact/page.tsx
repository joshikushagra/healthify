import { AppLayout } from "@/components/layout/app-layout"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Mail, Phone, MapPin, Clock, MessageSquare, Send, Calendar, HeadphonesIcon } from "lucide-react"

const contactMethods = [
  {
    icon: Phone,
    title: "Phone Support",
    description: "24/7 technical support",
    contact: "+1 (555) 123-4567",
    availability: "Available 24/7",
  },
  {
    icon: Mail,
    title: "Email Support",
    description: "General inquiries",
    contact: "support@healthify.com",
    availability: "Response within 2 hours",
  },
  {
    icon: MessageSquare,
    title: "Live Chat",
    description: "Instant assistance",
    contact: "Chat with our team",
    availability: "Mon-Fri, 8AM-8PM EST",
  },
  {
    icon: HeadphonesIcon,
    title: "Emergency Support",
    description: "Critical system issues",
    contact: "+1 (555) 911-HELP",
    availability: "Available 24/7",
  },
]

const offices = [
  {
    city: "New York",
    address: "123 Healthcare Ave, Suite 500",
    zipcode: "New York, NY 10001",
    phone: "+1 (555) 123-4567",
  },
  {
    city: "San Francisco",
    address: "456 Medical Center Blvd",
    zipcode: "San Francisco, CA 94102",
    phone: "+1 (555) 987-6543",
  },
  {
    city: "Chicago",
    address: "789 Innovation Drive",
    zipcode: "Chicago, IL 60601",
    phone: "+1 (555) 456-7890",
  },
]

export default function ContactPage() {
  return (
    <AppLayout userType="patient" userName="Guest" userEmail="">
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <MessageSquare className="w-6 h-6 text-primary-foreground" />
            </div>
            <h1 className="text-3xl font-bold text-foreground">Contact HEALTHIFY</h1>
          </div>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Get in touch with our team for support, partnerships, or general inquiries. We're here to help you make the
            most of our AI-powered healthcare platform.
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Contact Form */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Send className="w-5 h-5" />
                  Send us a Message
                </CardTitle>
                <CardDescription>Fill out the form below and we'll get back to you within 24 hours</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">First Name</label>
                    <Input placeholder="Enter your first name" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Last Name</label>
                    <Input placeholder="Enter your last name" />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Email</label>
                    <Input type="email" placeholder="your.email@example.com" />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Phone</label>
                    <Input type="tel" placeholder="+1 (555) 123-4567" />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Organization</label>
                  <Input placeholder="Your hospital, clinic, or organization" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Subject</label>
                  <Input placeholder="What can we help you with?" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Message</label>
                  <Textarea placeholder="Tell us more about your inquiry..." className="min-h-[120px]" />
                </div>

                <div className="flex gap-3">
                  <Button className="flex-1">
                    <Send className="w-4 h-4 mr-2" />
                    Send Message
                  </Button>
                  <Button variant="outline">
                    <Calendar className="w-4 h-4 mr-2" />
                    Schedule Call
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Contact Information */}
          <div className="space-y-6">
            {/* Contact Methods */}
            <Card>
              <CardHeader>
                <CardTitle>Get in Touch</CardTitle>
                <CardDescription>Multiple ways to reach our team</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {contactMethods.map((method) => {
                  const Icon = method.icon
                  return (
                    <div
                      key={method.title}
                      className="flex gap-3 p-3 border border-border rounded-lg hover:bg-muted/50 transition-colors"
                    >
                      <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Icon className="w-5 h-5 text-primary" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-medium text-sm">{method.title}</h3>
                        <p className="text-xs text-muted-foreground mb-1">{method.description}</p>
                        <p className="text-sm font-medium text-primary">{method.contact}</p>
                        <Badge variant="outline" className="text-xs mt-1">
                          {method.availability}
                        </Badge>
                      </div>
                    </div>
                  )
                })}
              </CardContent>
            </Card>

            {/* Office Locations */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MapPin className="w-5 h-5" />
                  Office Locations
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {offices.map((office) => (
                  <div key={office.city} className="p-3 border border-border rounded-lg">
                    <h3 className="font-medium text-sm mb-2">{office.city} Office</h3>
                    <div className="space-y-1 text-xs text-muted-foreground">
                      <p>{office.address}</p>
                      <p>{office.zipcode}</p>
                      <p className="text-primary font-medium">{office.phone}</p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Business Hours */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="w-5 h-5" />
                  Business Hours
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span>Monday - Friday</span>
                  <span className="font-medium">8:00 AM - 8:00 PM EST</span>
                </div>
                <div className="flex justify-between">
                  <span>Saturday</span>
                  <span className="font-medium">9:00 AM - 5:00 PM EST</span>
                </div>
                <div className="flex justify-between">
                  <span>Sunday</span>
                  <span className="font-medium">Emergency Support Only</span>
                </div>
                <div className="pt-2 border-t border-border">
                  <div className="flex justify-between">
                    <span>Emergency Support</span>
                    <Badge variant="secondary" className="text-xs">
                      24/7
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* FAQ Section */}
        <Card>
          <CardHeader>
            <CardTitle>Frequently Asked Questions</CardTitle>
            <CardDescription>Quick answers to common questions</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-medium mb-2">How do I get started with HEALTHIFY?</h3>
                <p className="text-sm text-muted-foreground">
                  Contact our sales team to schedule a demo and discuss your organization's needs.
                </p>
              </div>
              <div>
                <h3 className="font-medium mb-2">Is HEALTHIFY HIPAA compliant?</h3>
                <p className="text-sm text-muted-foreground">
                  Yes, we maintain full HIPAA compliance and enterprise-grade security standards.
                </p>
              </div>
              <div>
                <h3 className="font-medium mb-2">What kind of support do you offer?</h3>
                <p className="text-sm text-muted-foreground">
                  We provide 24/7 technical support, training, and ongoing customer success management.
                </p>
              </div>
              <div>
                <h3 className="font-medium mb-2">Can HEALTHIFY integrate with our existing systems?</h3>
                <p className="text-sm text-muted-foreground">
                  Yes, we offer comprehensive API integration with most major healthcare systems and EHRs.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </AppLayout>
  )
}
