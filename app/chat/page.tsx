"use client"
import { useState } from "react"
import type React from "react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import {
  Send,
  Bot,
  User,
  Stethoscope,
  Heart,
  Brain,
  Activity,
  MessageSquare,
  Sparkles,
  ArrowLeft,
  Loader2,
} from "lucide-react"
import Link from "next/link"

const suggestedQuestions = [
  "What are the symptoms of hypertension?",
  "How to interpret blood pressure readings?",
  "Common side effects of metformin?",
  "When to refer a patient to a cardiologist?",
  "Signs of diabetic ketoacidosis?",
  "How to calculate BMI and interpret results?",
]

const medicalSpecialties = [
  { icon: Heart, name: "Cardiology", color: "text-red-500" },
  { icon: Brain, name: "Neurology", color: "text-purple-500" },
  { icon: Activity, name: "Internal Medicine", color: "text-blue-500" },
  { icon: Stethoscope, name: "General Practice", color: "text-green-500" },
]

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  createdAt: Date
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      createdAt: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    // Simulate AI response (replace with your backend integration)
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "I'm a frontend-only demo. Please integrate with your preferred AI backend to enable real medical assistance. I can help with medical questions, drug interactions, and clinical guidance once connected to an AI service.",
        createdAt: new Date(),
      }
      setMessages((prev) => [...prev, aiMessage])
      setIsLoading(false)
    }, 1500)
  }

  const handleSuggestedQuestion = (question: string) => {
    setInput(question)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 lg:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="w-4 h-4 mr-2" />
                <span className="hidden sm:inline">Back to Home</span>
                <span className="sm:hidden">Back</span>
              </Button>
            </Link>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
                <Bot className="w-6 h-6 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-lg lg:text-xl font-semibold text-foreground">HEALTHIFY AI Assistant</h1>
                <p className="text-xs lg:text-sm text-muted-foreground">Frontend Demo - Connect Your AI Backend</p>
              </div>
            </div>
          </div>
          <Badge variant="secondary" className="gap-1">
            <Sparkles className="w-3 h-3" />
            AI Ready
          </Badge>
        </div>
      </header>

      <div className="container mx-auto px-4 lg:px-6 py-6 max-w-7xl">
        <div className="grid lg:grid-cols-4 gap-6 lg:gap-8 h-[calc(100vh-140px)]">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg lg:text-xl">Medical Specialties</CardTitle>
                <CardDescription className="text-sm lg:text-base">AI trained in various medical fields</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {medicalSpecialties.map((specialty) => {
                  const Icon = specialty.icon
                  return (
                    <div
                      key={specialty.name}
                      className="flex items-center gap-3 p-3 rounded-xl hover:bg-muted/50 transition-colors cursor-pointer"
                    >
                      <Icon className={`w-5 h-5 lg:w-6 lg:h-6 ${specialty.color}`} />
                      <span className="text-sm lg:text-base font-medium">{specialty.name}</span>
                    </div>
                  )
                })}
              </CardContent>
            </Card>

            <Card className="shadow-sm">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg lg:text-xl">Quick Questions</CardTitle>
                <CardDescription className="text-sm lg:text-base">Common medical queries</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                {suggestedQuestions.map((question, index) => (
                  <Button
                    key={index}
                    variant="ghost"
                    className="w-full text-left justify-start h-auto p-3 text-sm lg:text-base text-muted-foreground hover:text-foreground hover:bg-muted/50 rounded-xl"
                    onClick={() => handleSuggestedQuestion(question)}
                    disabled={isLoading}
                  >
                    <span className="line-clamp-2">{question}</span>
                  </Button>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Chat Interface */}
          <div className="lg:col-span-3 flex flex-col">
            <Card className="flex-1 flex flex-col shadow-sm">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <Avatar className="w-12 h-12">
                      <AvatarImage src="/ai-avatar.png" />
                      <AvatarFallback className="bg-primary text-primary-foreground">
                        <Bot className="w-6 h-6" />
                      </AvatarFallback>
                    </Avatar>
                    <div>
                      <h3 className="font-semibold text-lg lg:text-xl">HEALTHIFY AI Assistant</h3>
                      <p className="text-sm lg:text-base text-muted-foreground">
                        {isLoading ? "Thinking..." : "Frontend Demo • Connect Your Backend"}
                      </p>
                    </div>
                  </div>
                  <Badge variant="outline" className="gap-1">
                    <MessageSquare className="w-3 h-3" />
                    {messages.length} messages
                  </Badge>
                </div>
                <Separator />
              </CardHeader>

              <CardContent className="flex-1 flex flex-col p-0">
                <ScrollArea className="flex-1 px-4 lg:px-6">
                  <div className="space-y-6 py-4 max-w-none">
                    {messages.length === 0 && (
                      <div className="flex gap-4">
                        <Avatar className="w-10 h-10 flex-shrink-0">
                          <AvatarFallback className="bg-primary text-primary-foreground">
                            <Bot className="w-5 h-5" />
                          </AvatarFallback>
                        </Avatar>
                        <div className="flex-1 max-w-[calc(100%-4rem)]">
                          <div className="inline-block p-4 lg:p-6 rounded-xl bg-muted">
                            <p className="text-sm lg:text-base leading-relaxed text-foreground">
                              Hello! I'm your HEALTHIFY AI Assistant. This is a frontend demo - please connect your
                              preferred AI backend (OpenAI, Anthropic, etc.) to enable real medical assistance. I can
                              help with medical questions, drug interactions, diagnostic guidance, and clinical decision
                              support once connected.
                            </p>
                          </div>
                          <p className="text-xs text-muted-foreground mt-2">Just now</p>
                        </div>
                      </div>
                    )}

                    {messages.map((message) => (
                      <div
                        key={message.id}
                        className={`flex gap-4 ${message.role === "user" ? "flex-row-reverse" : "flex-row"}`}
                      >
                        <Avatar className="w-10 h-10 flex-shrink-0">
                          {message.role === "user" ? (
                            <AvatarFallback className="bg-secondary">
                              <User className="w-5 h-5" />
                            </AvatarFallback>
                          ) : (
                            <AvatarFallback className="bg-primary text-primary-foreground">
                              <Bot className="w-5 h-5" />
                            </AvatarFallback>
                          )}
                        </Avatar>
                        <div
                          className={`flex-1 max-w-[calc(100%-4rem)] ${message.role === "user" ? "text-right" : "text-left"}`}
                        >
                          <div
                            className={`inline-block p-4 lg:p-6 rounded-xl max-w-full ${
                              message.role === "user"
                                ? "bg-primary text-primary-foreground"
                                : "bg-muted text-foreground"
                            }`}
                          >
                            <p className="text-sm lg:text-base leading-relaxed whitespace-pre-wrap break-words">
                              {message.content}
                            </p>
                          </div>
                          <p className="text-xs text-muted-foreground mt-2">{message.createdAt.toLocaleTimeString()}</p>
                        </div>
                      </div>
                    ))}

                    {isLoading && (
                      <div className="flex gap-4">
                        <Avatar className="w-10 h-10 flex-shrink-0">
                          <AvatarFallback className="bg-primary text-primary-foreground">
                            <Bot className="w-5 h-5" />
                          </AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <div className="inline-block p-4 lg:p-6 rounded-xl bg-muted">
                            <div className="flex items-center gap-3">
                              <Loader2 className="w-5 h-5 animate-spin" />
                              <span className="text-sm lg:text-base text-muted-foreground">AI is thinking...</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </ScrollArea>

                <div className="p-4 lg:p-6 border-t border-border">
                  <form onSubmit={handleSubmit} className="flex gap-3">
                    <Input
                      placeholder="Ask me anything about medicine, symptoms, treatments..."
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      className="flex-1 h-12 text-base"
                      disabled={isLoading}
                    />
                    <Button type="submit" disabled={isLoading || !input.trim()} size="lg" className="px-6">
                      {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                    </Button>
                  </form>
                  <p className="text-xs lg:text-sm text-muted-foreground mt-3 text-center leading-relaxed">
                    Frontend demo only. Connect your AI backend for real medical assistance. Always consult healthcare
                    professionals for medical advice.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
