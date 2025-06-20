"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/UI/Card"
import  Button  from "@/components/UI/Button"
import { Badge } from "@/components/UI/Badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/UI/Tabs"
import {
  Camera,
  CameraOff,
  Volume2,
  VolumeX,
  Play,
  Pause,
  RotateCcw,
  Settings,
  BookOpen,
  Target,
  TrendingUp,
  Hand,
  Brain,
  Eye,
  Languages,
  Loader2,
} from "lucide-react"

// Sign Language Dictionary with Hindi and English translations
const signDictionary = [
  {
    id: 1,
    sign: "hello",
    emoji: "👋",
    english: "Hello",
    hindi: "नमस्ते",
    hindiPronunciation: "namaste",
    description: "Wave hand side to side",
    difficulty: "easy",
    category: "greetings",
  },
  {
    id: 2,
    sign: "thank_you",
    emoji: "🙏",
    english: "Thank you",
    hindi: "धन्यवाद",
    hindiPronunciation: "dhanyawad",
    description: "Touch chin, move hand forward",
    difficulty: "easy",
    category: "greetings",
  },
  {
    id: 3,
    sign: "please",
    emoji: "🤲",
    english: "Please",
    hindi: "कृपया",
    hindiPronunciation: "kripaya",
    description: "Flat hand on chest, circular motion",
    difficulty: "easy",
    category: "greetings",
  },
  {
    id: 4,
    sign: "love",
    emoji: "❤️",
    english: "Love",
    hindi: "प्रेम",
    hindiPronunciation: "prem",
    description: "Cross arms over chest",
    difficulty: "medium",
    category: "emotions",
  },
  {
    id: 5,
    sign: "family",
    emoji: "👨‍👩‍👧‍👦",
    english: "Family",
    hindi: "परिवार",
    hindiPronunciation: "parivar",
    description: "F handshape, circle motion",
    difficulty: "medium",
    category: "relationships",
  },
  {
    id: 6,
    sign: "friend",
    emoji: "🤝",
    english: "Friend",
    hindi: "मित्र",
    hindiPronunciation: "mitra",
    description: "Hook index fingers together",
    difficulty: "easy",
    category: "relationships",
  },
  {
    id: 7,
    sign: "water",
    emoji: "💧",
    english: "Water",
    hindi: "पानी",
    hindiPronunciation: "paani",
    description: "W handshape at mouth",
    difficulty: "easy",
    category: "basic_needs",
  },
  {
    id: 8,
    sign: "food",
    emoji: "🍎",
    english: "Food",
    hindi: "खाना",
    hindiPronunciation: "khana",
    description: "Fingertips to mouth",
    difficulty: "easy",
    category: "basic_needs",
  },
  {
    id: 9,
    sign: "home",
    emoji: "🏠",
    english: "Home",
    hindi: "घर",
    hindiPronunciation: "ghar",
    description: "Fingertips touch, then separate",
    difficulty: "medium",
    category: "places",
  },
  {
    id: 10,
    sign: "school",
    emoji: "🏫",
    english: "School",
    hindi: "स्कूल",
    hindiPronunciation: "school",
    description: "Clap hands twice",
    difficulty: "medium",
    category: "places",
  },
  {
    id: 11,
    sign: "happy",
    emoji: "😊",
    english: "Happy",
    hindi: "खुश",
    hindiPronunciation: "khush",
    description: "Brush chest upward twice",
    difficulty: "easy",
    category: "emotions",
  },
  {
    id: 12,
    sign: "sad",
    emoji: "😢",
    english: "Sad",
    hindi: "उदास",
    hindiPronunciation: "udaas",
    description: "Fingers down face like tears",
    difficulty: "easy",
    category: "emotions",
  },
  {
    id: 13,
    sign: "good",
    emoji: "👍",
    english: "Good",
    hindi: "अच्छा",
    hindiPronunciation: "accha",
    description: "Thumb up from chin",
    difficulty: "easy",
    category: "descriptive",
  },
  {
    id: 14,
    sign: "bad",
    emoji: "👎",
    english: "Bad",
    hindi: "बुरा",
    hindiPronunciation: "bura",
    description: "Fingertips to chin, flip down",
    difficulty: "easy",
    category: "descriptive",
  },
  {
    id: 15,
    sign: "yes",
    emoji: "✅",
    english: "Yes",
    hindi: "हाँ",
    hindiPronunciation: "haan",
    description: "Fist nod up and down",
    difficulty: "easy",
    category: "responses",
  },
  {
    id: 16,
    sign: "no",
    emoji: "❌",
    english: "No",
    hindi: "नहीं",
    hindiPronunciation: "nahin",
    description: "Index and middle finger close",
    difficulty: "easy",
    category: "responses",
  },
  {
    id: 17,
    sign: "help",
    emoji: "🆘",
    english: "Help",
    hindi: "मदद",
    hindiPronunciation: "madad",
    description: "Fist on flat palm, lift up",
    difficulty: "medium",
    category: "actions",
  },
  {
    id: 18,
    sign: "sorry",
    emoji: "😔",
    english: "Sorry",
    hindi: "माफ़ करना",
    hindiPronunciation: "maaf karna",
    description: "Fist circle on chest",
    difficulty: "medium",
    category: "greetings",
  },
  {
    id: 19,
    sign: "beautiful",
    emoji: "🌸",
    english: "Beautiful",
    hindi: "सुंदर",
    hindiPronunciation: "sundar",
    description: "5 handshape around face, close to 9",
    difficulty: "hard",
    category: "descriptive",
  },
  {
    id: 20,
    sign: "mother",
    emoji: "👩",
    english: "Mother",
    hindi: "माँ",
    hindiPronunciation: "maa",
    description: "Thumb to chin",
    difficulty: "easy",
    category: "relationships",
  },
  {
    id: 21,
    sign: "father",
    emoji: "👨",
    english: "Father",
    hindi: "पिता",
    hindiPronunciation: "pita",
    description: "Thumb to forehead",
    difficulty: "easy",
    category: "relationships",
  },
  {
    id: 22,
    sign: "work",
    emoji: "💼",
    english: "Work",
    hindi: "काम",
    hindiPronunciation: "kaam",
    description: "Fist tap wrist twice",
    difficulty: "medium",
    category: "actions",
  },
  {
    id: 23,
    sign: "play",
    emoji: "🎮",
    english: "Play",
    hindi: "खेलना",
    hindiPronunciation: "khelna",
    description: "Y handshapes shake",
    difficulty: "easy",
    category: "actions",
  },
  {
    id: 24,
    sign: "learn",
    emoji: "📚",
    english: "Learn",
    hindi: "सीखना",
    hindiPronunciation: "seekhna",
    description: "Fingertips to forehead, then out",
    difficulty: "medium",
    category: "actions",
  },
  {
    id: 25,
    sign: "understand",
    emoji: "💡",
    english: "Understand",
    hindi: "समझना",
    hindiPronunciation: "samajhna",
    description: "Index finger flick at temple",
    difficulty: "medium",
    category: "mental",
  },
]

interface DetectedSign {
  id: number
  sign: string
  confidence: number
  timestamp: number
  english: string
  hindi: string
  hindiPronunciation: string
  emoji: string
}

type SignLanguageReaderProps = {}

export default function SignLanguageReader({}: SignLanguageReaderProps) {
  const [isReading, setIsReading] = useState(false)
  const [cameraActive, setCameraActive] = useState(false)
  const [currentLanguage, setCurrentLanguage] = useState<"english" | "hindi" | "both">("both")
  const [speechEnabled, setSpeechEnabled] = useState(true)
  const [detectedSigns, setDetectedSigns] = useState<DetectedSign[]>([])
  const [currentSign, setCurrentSign] = useState<DetectedSign | null>(null)
  const [sessionStats, setSessionStats] = useState({
    signsDetected: 0,
    accuracy: 0,
    sessionTime: 0,
    streak: 0,
  })
  const [selectedCategory, setSelectedCategory] = useState<string>("all")
  const [currentLearningSign, setCurrentLearningSign] = useState(0)
  const [isProcessing, setIsProcessing] = useState(false)

  const videoRef = useRef<HTMLVideoElement>(null)
  const streamRef = useRef<MediaStream | null>(null)
  const sessionTimerRef = useRef<NodeJS.Timeout | null>(null)
  const detectionIntervalRef = useRef<NodeJS.Timeout | null>(null)

  // Categories for filtering
  const categories = [
    "all",
    "greetings",
    "emotions",
    "relationships",
    "basic_needs",
    "places",
    "descriptive",
    "responses",
    "actions",
    "mental",
  ]

  // Get filtered signs based on category
  const getFilteredSigns = () => {
    if (selectedCategory === "all") return signDictionary
    return signDictionary.filter((sign) => sign.category === selectedCategory)
  }

  // Text-to-Speech function
  const speakText = useCallback(
    (text: string, language: "en" | "hi") => {
      if (!speechEnabled || !("speechSynthesis" in window)) return

      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = language === "en" ? "en-US" : "hi-IN"
      utterance.rate = 0.8
      utterance.pitch = 1
      utterance.volume = 0.8

      // Get available voices
      const voices = speechSynthesis.getVoices()
      const voice = voices.find((v) => v.lang.startsWith(language === "en" ? "en" : "hi"))
      if (voice) utterance.voice = voice

      speechSynthesis.speak(utterance)
    },
    [speechEnabled],
  )

  // Simulate sign detection (in real app, this would use ML model)
  const simulateSignDetection = useCallback(() => {
    if (!isReading || !cameraActive) return

    setIsProcessing(true)

    setTimeout(
      () => {
        const filteredSigns = getFilteredSigns()
        const randomSign = filteredSigns[Math.floor(Math.random() * filteredSigns.length)]
        const confidence = Math.random() * 0.4 + 0.6 // 60-100% confidence

        const detectedSign: DetectedSign = {
          id: randomSign.id,
          sign: randomSign.sign,
          confidence,
          timestamp: Date.now(),
          english: randomSign.english,
          hindi: randomSign.hindi,
          hindiPronunciation: randomSign.hindiPronunciation,
          emoji: randomSign.emoji,
        }

        setCurrentSign(detectedSign)
        setDetectedSigns((prev) => [detectedSign, ...prev.slice(0, 9)]) // Keep last 10

        // Update stats
        setSessionStats((prev) => ({
          ...prev,
          signsDetected: prev.signsDetected + 1,
          accuracy: (prev.accuracy + confidence) / 2,
          streak: confidence > 0.7 ? prev.streak + 1 : 0,
        }))

        // Speak the detected sign
        if (currentLanguage === "english") {
          speakText(detectedSign.english, "en")
        } else if (currentLanguage === "hindi") {
          speakText(detectedSign.hindi, "hi")
        } else {
          // Both languages
          speakText(detectedSign.english, "en")
          setTimeout(() => speakText(detectedSign.hindi, "hi"), 1500)
        }

        setIsProcessing(false)
      },
      1000 + Math.random() * 2000,
    ) // Random delay 1-3 seconds
  }, [isReading, cameraActive, currentLanguage, speakText, selectedCategory])

  // Start camera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: 640,
          height: 480,
          facingMode: "user",
        },
      })

      if (videoRef.current) {
        videoRef.current.srcObject = stream
        streamRef.current = stream
        setCameraActive(true)
      }
    } catch (error) {
      console.error("Error accessing camera:", error)
      alert("Please allow camera access to use sign language reader.")
    }
  }

  // Stop camera
  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop())
      streamRef.current = null
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null
    }
    setCameraActive(false)
  }

  // Start reading signs
  const startReading = () => {
    if (!cameraActive) {
      startCamera()
    }
    setIsReading(true)
    setDetectedSigns([])
    setCurrentSign(null)

    // Start session timer
    sessionTimerRef.current = setInterval(() => {
      setSessionStats((prev) => ({ ...prev, sessionTime: prev.sessionTime + 1 }))
    }, 1000)

    // Start detection simulation
    detectionIntervalRef.current = setInterval(simulateSignDetection, 3000)
  }

  // Stop reading signs
  const stopReading = () => {
    setIsReading(false)

    if (sessionTimerRef.current) {
      clearInterval(sessionTimerRef.current)
      sessionTimerRef.current = null
    }

    if (detectionIntervalRef.current) {
      clearInterval(detectionIntervalRef.current)
      detectionIntervalRef.current = null
    }
  }

  // Reset session
  const resetSession = () => {
    stopReading()
    setDetectedSigns([])
    setCurrentSign(null)
    setSessionStats({
      signsDetected: 0,
      accuracy: 0,
      sessionTime: 0,
      streak: 0,
    })
  }

  // Format time
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
  }

  // Get confidence color
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return "text-green-600 bg-green-100"
    if (confidence >= 0.6) return "text-yellow-600 bg-yellow-100"
    return "text-red-600 bg-red-100"
  }

  // Learning mode functions
  const nextLearningSign = () => {
    setCurrentLearningSign((prev) => (prev + 1) % signDictionary.length)
  }

  const prevLearningSign = () => {
    setCurrentLearningSign((prev) => (prev - 1 + signDictionary.length) % signDictionary.length)
  }

  const speakLearningSign = (language: "en" | "hi") => {
    const sign = signDictionary[currentLearningSign]
    speakText(language === "en" ? sign.english : sign.hindi, language)
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopReading()
      stopCamera()
    }
  }, [])

  // Run detection simulation
  useEffect(() => {
    if (isReading && cameraActive) {
      simulateSignDetection()
    }
  }, [simulateSignDetection])

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-orange-50 to-rose-50 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-600 to-orange-500 bg-clip-text text-transparent mb-4">
            🤟 Sign Language Reader
          </h1>
          <p className="text-pink-600 text-xl">AI-powered sign language to speech converter in Hindi & English</p>
          <div className="flex justify-center gap-4 mt-4">
            <div className="flex items-center gap-2 text-2xl">
              <span>👁️</span>
              <span>🤟</span>
              <span>🗣️</span>
              <span>🇮🇳</span>
              <span>🇺🇸</span>
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <Card className="mb-8 border-pink-200 bg-gradient-to-r from-pink-100 via-orange-100 to-rose-100 shadow-xl">
          <CardHeader className="pb-6">
            <CardTitle className="flex items-center gap-3 text-pink-800 text-2xl">
              <TrendingUp className="w-6 h-6" />
              Session Statistics
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              <div className="text-center bg-white rounded-lg p-4 shadow-md">
                <div className="text-3xl font-bold text-pink-700">{sessionStats.signsDetected}</div>
                <div className="text-sm text-pink-600">Signs Detected 🤟</div>
              </div>
              <div className="text-center bg-white rounded-lg p-4 shadow-md">
                <div className="text-3xl font-bold text-orange-700">{Math.round(sessionStats.accuracy * 100)}%</div>
                <div className="text-sm text-orange-600">Accuracy ⭐</div>
              </div>
              <div className="text-center bg-white rounded-lg p-4 shadow-md">
                <div className="text-3xl font-bold text-rose-700">{formatTime(sessionStats.sessionTime)}</div>
                <div className="text-sm text-rose-600">Session Time ⏱️</div>
              </div>
              <div className="text-center bg-white rounded-lg p-4 shadow-md">
                <div className="text-3xl font-bold text-pink-700">{sessionStats.streak}</div>
                <div className="text-sm text-pink-600">Streak 🔥</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Main Interface */}
        <Tabs defaultValue="reader" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-pink-100 mb-8 h-auto shadow-lg">
            <TabsTrigger value="reader" className="data-[state=active]:bg-rose-200 p-6 text-xl font-semibold">
              <Eye className="w-6 h-6 mr-3" />
              Sign Reader
            </TabsTrigger>
            <TabsTrigger value="learning" className="data-[state=active]:bg-rose-200 p-6 text-xl font-semibold">
              <BookOpen className="w-6 h-6 mr-3" />
              Learning Mode
            </TabsTrigger>
          </TabsList>

          {/* Sign Reader Tab */}
          <TabsContent value="reader">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Camera Feed */}
              <Card className="border-pink-200 shadow-xl">
                <CardHeader className="bg-gradient-to-r from-pink-100 to-orange-100">
                  <CardTitle className="text-pink-800 text-2xl flex items-center gap-3">
                    <Camera className="w-6 h-6" />
                    Camera Feed
                  </CardTitle>
                  <CardDescription className="text-pink-600">
                    Position your hands in view for sign detection
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-6">
                  <div className="relative bg-gradient-to-br from-gray-100 to-gray-200 rounded-2xl overflow-hidden aspect-video shadow-lg mb-6">
                    <video ref={videoRef} autoPlay muted className="w-full h-full object-cover" />
                    {!cameraActive && (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-center">
                          <Camera className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                          <p className="text-gray-500 text-lg">Camera not active</p>
                        </div>
                      </div>
                    )}

                    {/* Detection Overlay */}
                    {isReading && cameraActive && (
                      <div className="absolute top-4 left-4 right-4">
                        <div className="bg-pink-500 text-white p-3 rounded-lg flex items-center gap-3">
                          <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
                          <span className="font-semibold">Detecting signs...</span>
                          {isProcessing && <Loader2 className="w-4 h-4 animate-spin" />}
                        </div>
                      </div>
                    )}

                    {/* Current Detection */}
                    {currentSign && (
                      <div className="absolute bottom-4 left-4 right-4">
                        <div className="bg-white/90 backdrop-blur-sm p-4 rounded-lg">
                          <div className="flex items-center gap-3">
                            <div className="text-3xl">{currentSign.emoji}</div>
                            <div className="flex-1">
                              <div className="font-bold text-gray-800">{currentSign.english}</div>
                              <div className="text-pink-600">{currentSign.hindi}</div>
                            </div>
                            <Badge className={`${getConfidenceColor(currentSign.confidence)} border-0`}>
                              {Math.round(currentSign.confidence * 100)}%
                            </Badge>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Controls */}
                  <div className="flex flex-wrap justify-center gap-4">
                    <Button
                      onClick={cameraActive ? stopCamera : startCamera}
                      className="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white px-6 py-3"
                    >
                      {cameraActive ? <CameraOff className="w-5 h-5 mr-2" /> : <Camera className="w-5 h-5 mr-2" />}
                      {cameraActive ? "Stop Camera" : "Start Camera"}
                    </Button>

                    <Button
                      onClick={isReading ? stopReading : startReading}
                      disabled={!cameraActive}
                      className="bg-gradient-to-r from-orange-500 to-pink-500 hover:from-orange-600 hover:to-pink-600 text-white px-6 py-3"
                    >
                      {isReading ? <Pause className="w-5 h-5 mr-2" /> : <Play className="w-5 h-5 mr-2" />}
                      {isReading ? "Stop Reading" : "Start Reading"}
                    </Button>

                    <Button
                      onClick={resetSession}
                      variant="outline"
                      className="border-pink-300 text-pink-700 px-6 py-3"
                    >
                      <RotateCcw className="w-5 h-5 mr-2" />
                      Reset
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Detection Results */}
              <Card className="border-pink-200 shadow-xl">
                <CardHeader className="bg-gradient-to-r from-orange-100 to-rose-100">
                  <CardTitle className="text-pink-800 text-2xl flex items-center gap-3">
                    <Brain className="w-6 h-6" />
                    Detection Results
                  </CardTitle>
                  <CardDescription className="text-pink-600">Real-time sign language recognition</CardDescription>
                </CardHeader>
                <CardContent className="p-6">
                  {detectedSigns.length > 0 ? (
                    <div className="space-y-3 max-h-96 overflow-y-auto">
                      {detectedSigns.map((sign, index) => (
                        <div
                          key={`${sign.id}-${sign.timestamp}`}
                          className={`p-4 rounded-lg border transition-all duration-300 ${
                            index === 0
                              ? "bg-gradient-to-r from-pink-100 to-orange-100 border-pink-300 shadow-md"
                              : "bg-white border-gray-200"
                          }`}
                        >
                          <div className="flex items-center gap-4">
                            <div className="text-2xl">{sign.emoji}</div>
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="font-bold text-gray-800">{sign.english}</span>
                                <Badge className={`${getConfidenceColor(sign.confidence)} border-0 text-xs`}>
                                  {Math.round(sign.confidence * 100)}%
                                </Badge>
                              </div>
                              <div className="text-pink-600 text-sm">{sign.hindi}</div>
                              <div className="text-gray-500 text-xs">({sign.hindiPronunciation})</div>
                            </div>
                            <div className="flex gap-2">
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => speakText(sign.english, "en")}
                                className="border-blue-300 text-blue-700 bg-white"
                              >
                                🇺🇸
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => speakText(sign.hindi, "hi")}
                                className="border-orange-300 text-orange-700 bg-white"
                              >
                                🇮🇳
                              </Button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-12">
                      <Hand className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                      <p className="text-gray-500 text-lg">No signs detected yet</p>
                      <p className="text-gray-400">Start the camera and begin signing!</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Settings Panel */}
            <Card className="mt-8 border-pink-200 shadow-xl">
              <CardHeader className="bg-gradient-to-r from-pink-100 to-orange-100">
                <CardTitle className="text-pink-800 text-2xl flex items-center gap-3">
                  <Settings className="w-6 h-6" />
                  Settings & Preferences
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  {/* Language Settings */}
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                      <Languages className="w-5 h-5" />
                      Speech Language
                    </h3>
                    <div className="space-y-2">
                      {[
                        { value: "english", label: "English Only 🇺🇸", icon: "🇺🇸" },
                        { value: "hindi", label: "Hindi Only 🇮🇳", icon: "🇮🇳" },
                        { value: "both", label: "Both Languages 🌍", icon: "🌍" },
                      ].map((option) => (
                        <Button
                          key={option.value}
                          variant={currentLanguage === option.value ? "primary" : "outline"}
                          className={`w-full justify-start ${
                            currentLanguage === option.value
                              ? "bg-gradient-to-r from-pink-500 to-orange-500 text-white"
                              : "border-pink-300 text-pink-700 bg-white"
                          }`}
                          onClick={() => setCurrentLanguage(option.value as "english" | "hindi" | "both")}
                        >
                          <span className="mr-2">{option.icon}</span>
                          {option.label}
                        </Button>
                      ))}
                    </div>
                  </div>

                  {/* Category Filter */}
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                      <Target className="w-5 h-5" />
                      Sign Category
                    </h3>
                    <div className="space-y-2 max-h-40 overflow-y-auto">
                      {categories.map((category) => (
                        <Button
                          key={category}
                          variant={selectedCategory === category ? "primary" : "outline"}
                          size="sm"
                          className={`w-full justify-start text-xs ${
                            selectedCategory === category
                              ? "bg-gradient-to-r from-orange-500 to-pink-500 text-white"
                              : "border-orange-300 text-orange-700 bg-white"
                          }`}
                          onClick={() => setSelectedCategory(category)}
                        >
                          {category.replace("_", " ").toUpperCase()}
                        </Button>
                      ))}
                    </div>
                  </div>

                  {/* Audio Settings */}
                  <div>
                    <h3 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                      <Volume2 className="w-5 h-5" />
                      Audio Settings
                    </h3>
                    <div className="space-y-3">
                      <Button
                        variant={speechEnabled ? "primary" : "outline"}
                        className={`w-full justify-start ${
                          speechEnabled
                            ? "bg-gradient-to-r from-green-500 to-blue-500 text-white"
                            : "border-gray-300 text-gray-700 bg-white"
                        }`}
                        onClick={() => setSpeechEnabled(!speechEnabled)}
                      >
                        {speechEnabled ? <Volume2 className="w-4 h-4 mr-2" /> : <VolumeX className="w-4 h-4 mr-2" />}
                        Speech {speechEnabled ? "Enabled" : "Disabled"}
                      </Button>

                      <div className="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                        <p className="font-medium mb-1">💡 Tips:</p>
                        <ul className="text-xs space-y-1">
                          <li>• Ensure good lighting for better detection</li>
                          <li>• Keep hands clearly visible in frame</li>
                          <li>• Sign at a moderate pace</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Learning Mode Tab */}
          <TabsContent value="learning">
            <Card className="border-pink-200 shadow-xl">
              <CardHeader className="bg-gradient-to-r from-pink-100 to-orange-100">
                <CardTitle className="text-pink-800 text-2xl flex items-center gap-3">
                  <BookOpen className="w-6 h-6" />
                  Sign Language Dictionary
                </CardTitle>
                <CardDescription className="text-pink-600">
                  Learn signs with audio pronunciation in both languages
                </CardDescription>
              </CardHeader>
              <CardContent className="p-8">
                <div className="text-center mb-8">
                  <div className="text-8xl mb-6">{signDictionary[currentLearningSign].emoji}</div>
                  <h2 className="text-4xl font-bold text-pink-800 mb-4">
                    {signDictionary[currentLearningSign].english}
                  </h2>
                  <h3 className="text-3xl font-bold text-orange-700 mb-2">
                    {signDictionary[currentLearningSign].hindi}
                  </h3>
                  <p className="text-lg text-gray-600 mb-6">
                    ({signDictionary[currentLearningSign].hindiPronunciation})
                  </p>

                  <div className="flex flex-wrap justify-center gap-3 mb-6">
                    <Badge variant="default" className="bg-pink-100 text-pink-700 text-lg px-4 py-2">
                      {signDictionary[currentLearningSign].category.replace("_", " ")}
                    </Badge>
                    <Badge
                      variant={
                        signDictionary[currentLearningSign].difficulty === "easy"
                          ? "default"
                          : signDictionary[currentLearningSign].difficulty === "medium"
                            ? "secondary"
                            : "destructive"
                      }
                      className="text-lg px-4 py-2"
                    >
                      {signDictionary[currentLearningSign].difficulty}
                    </Badge>
                  </div>

                  <div className="bg-rose-50 border-2 border-rose-200 rounded-xl p-6 mb-8">
                    <p className="text-rose-700 text-xl font-bold mb-2">🤟 How to Sign:</p>
                    <p className="text-rose-600 text-lg">{signDictionary[currentLearningSign].description}</p>
                  </div>

                  {/* Audio Buttons */}
                  <div className="flex justify-center gap-4 mb-8">
                    <Button
                      onClick={() => speakLearningSign("en")}
                      className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-8 py-3 text-lg"
                    >
                      <Volume2 className="w-5 h-5 mr-2" />
                      🇺🇸 English
                    </Button>
                    <Button
                      onClick={() => speakLearningSign("hi")}
                      className="bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white px-8 py-3 text-lg"
                    >
                      <Volume2 className="w-5 h-5 mr-2" />
                      🇮🇳 Hindi
                    </Button>
                  </div>

                  {/* Navigation */}
                  <div className="flex justify-center gap-4">
                    <Button
                      onClick={prevLearningSign}
                      variant="outline"
                      className="border-pink-300 text-pink-700 px-6 py-3 text-lg bg-white"
                    >
                      ← Previous
                    </Button>
                    <Button
                      onClick={nextLearningSign}
                      className="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 text-white px-6 py-3 text-lg"
                    >
                      Next →
                    </Button>
                  </div>

                  <div className="mt-6 text-sm text-gray-600">
                    Sign {currentLearningSign + 1} of {signDictionary.length}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Sign Dictionary Grid */}
            <Card className="mt-8 border-pink-200 shadow-xl">
              <CardHeader className="bg-gradient-to-r from-orange-100 to-rose-100">
                <CardTitle className="text-pink-800 text-2xl text-center">📚 Complete Sign Dictionary</CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                <div className="grid grid-cols-3 md:grid-cols-6 lg:grid-cols-8 gap-4">
                  {signDictionary.map((sign, index) => (
                    <div
                      key={sign.id}
                      className={`text-center p-3 rounded-lg hover:shadow-md transition-all cursor-pointer transform hover:scale-105 ${
                        index === currentLearningSign
                          ? "bg-gradient-to-br from-pink-100 to-orange-100 border-2 border-pink-300"
                          : "bg-gradient-to-br from-pink-50 to-rose-50"
                      }`}
                      onClick={() => setCurrentLearningSign(index)}
                    >
                      <div className="text-2xl mb-1">{sign.emoji}</div>
                      <div className="text-xs text-pink-600 font-medium">{sign.english}</div>
                      <div className="text-xs text-orange-600">{sign.hindi}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
