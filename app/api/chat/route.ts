import { openai } from "@ai-sdk/openai"
import { convertToModelMessages, streamText, type UIMessage, type CoreMessage } from "ai"

export const runtime = "edge"

export const maxDuration = 30

export async function POST(req: Request) {
  try {
    const { messages }: { messages: UIMessage[] } = await req.json()

    const converted: CoreMessage[] = convertToModelMessages(messages)

    const prompt: CoreMessage[] = [
      {
        role: "system",
        content: `You are a medical AI assistant designed to help healthcare professionals and patients with medical information. 

IMPORTANT GUIDELINES:
- Always emphasize that your responses are for informational purposes only
- Remind users to consult qualified healthcare professionals for medical advice
- Never provide specific diagnoses or treatment recommendations
- Focus on general medical knowledge, symptoms, and when to seek professional care
- Be helpful but cautious with medical information
- If asked about emergencies, always recommend immediate medical attention

You can help with:
- General medical information and education
- Symptom descriptions and when to see a doctor
- Medication information (general, not specific dosing)
- Health and wellness guidance
- Medical terminology explanations
- Preventive care recommendations

Always maintain a professional, caring, and informative tone.`,
      },
      ...converted,
    ]

    const result = streamText({
      model: openai("gpt-4o-mini"),
      messages: prompt,
      temperature: 0.7,
      abortSignal: req.signal,
    })

    return result.toTextStreamResponse()
  } catch (error) {
    console.error("Chat API error:", error)
    return new Response(JSON.stringify({ error: "Failed to process chat request" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    })
  }
}
