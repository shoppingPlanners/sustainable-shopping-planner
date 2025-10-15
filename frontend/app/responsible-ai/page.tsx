"use client";

import { Navigation } from "@/components/navigation"
import { Shield, Eye, Scale, Leaf, Lock, Users, FileCheck, AlertCircle } from "lucide-react"
import Link from "next/link"

export default function ResponsibleAIPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/20">
      <Navigation />
      
      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-100 dark:bg-green-900 mb-6">
            <Shield className="h-8 w-8 text-green-600 dark:text-green-400" />
          </div>
          <h1 className="text-4xl font-bold mb-4">Responsible AI Compliance</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Our commitment to ethical, transparent, and sustainable AI practices
          </p>
        </div>

        {/* Core Principles */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8 flex items-center gap-2">
            <FileCheck className="h-6 w-6 text-primary" />
            Our Core AI Principles
          </h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="p-6 rounded-lg border bg-card">
              <div className="flex items-start gap-4">
                <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900">
                  <Eye className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Transparency</h3>
                  <p className="text-sm text-muted-foreground">
                    All recommendations and sustainability scores are explainable with clear reasoning and weighted factors.
                  </p>
                </div>
              </div>
            </div>

            <div className="p-6 rounded-lg border bg-card">
              <div className="flex items-start gap-4">
                <div className="p-2 rounded-lg bg-purple-100 dark:bg-purple-900">
                  <Lock className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Privacy First</h3>
                  <p className="text-sm text-muted-foreground">
                    User data is anonymized, encrypted, and securely stored. We comply with GDPR and privacy best practices.
                  </p>
                </div>
              </div>
            </div>

            <div className="p-6 rounded-lg border bg-card">
              <div className="flex items-start gap-4">
                <div className="p-2 rounded-lg bg-amber-100 dark:bg-amber-900">
                  <Scale className="h-5 w-5 text-amber-600 dark:text-amber-400" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Fairness & Equity</h3>
                  <p className="text-sm text-muted-foreground">
                    Our algorithms are designed to avoid bias and provide equitable recommendations across all user segments.
                  </p>
                </div>
              </div>
            </div>

            <div className="p-6 rounded-lg border bg-card">
              <div className="flex items-start gap-4">
                <div className="p-2 rounded-lg bg-green-100 dark:bg-green-900">
                  <Leaf className="h-5 w-5 text-green-600 dark:text-green-400" />
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Sustainability Focus</h3>
                  <p className="text-sm text-muted-foreground">
                    AI agents prioritize eco-friendly products and sustainable brands in all recommendations.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* AI Agents Compliance */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8 flex items-center gap-2">
            <Users className="h-6 w-6 text-primary" />
            Our AI Agents: How They're Responsible & Compliant
          </h2>

          <div className="space-y-8">
            {/* Agent 1: User Behavior Tracker */}
            <div className="p-8 rounded-lg border bg-card shadow-sm">
              <div className="flex items-start gap-4 mb-4">
                <div className="p-3 rounded-lg bg-blue-100 dark:bg-blue-900">
                  <Users className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">1. User Behavior Tracker Agent</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Analyzes user interactions to improve personalization while respecting privacy
                  </p>
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4 ml-16">
                <div>
                  <h4 className="font-medium text-sm mb-2 text-green-600 dark:text-green-400">✓ Compliance Measures:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Data anonymization at collection</li>
                    <li>• Encrypted storage (AES-256)</li>
                    <li>• User consent management</li>
                    <li>• GDPR Article 6 & 7 compliant</li>
                    <li>• Opt-out available anytime</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-sm mb-2 text-blue-600 dark:text-blue-400">⚙️ How It Works:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Tracks page views & interactions</li>
                    <li>• Identifies preference patterns</li>
                    <li>• No personal data tracking</li>
                    <li>• Session-based analytics only</li>
                    <li>• 30-day data retention policy</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Agent 2: Recommendation Engine */}
            <div className="p-8 rounded-lg border bg-card shadow-sm">
              <div className="flex items-start gap-4 mb-4">
                <div className="p-3 rounded-lg bg-purple-100 dark:bg-purple-900">
                  <Leaf className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">2. Recommendation Engine (Suggestion Agent)</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Provides personalized sustainable product recommendations with explainable AI
                  </p>
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4 ml-16">
                <div>
                  <h4 className="font-medium text-sm mb-2 text-green-600 dark:text-green-400">✓ Compliance Measures:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Explainable scoring algorithm</li>
                    <li>• Bias testing & mitigation</li>
                    <li>• Transparent match reasons</li>
                    <li>• No discriminatory factors</li>
                    <li>• Regular fairness audits</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-sm mb-2 text-blue-600 dark:text-blue-400">⚙️ How It Works:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• 8 weighted scoring factors</li>
                    <li>• Category, budget, sustainability matching</li>
                    <li>• Rating & bestseller bonuses</li>
                    <li>• Shows detailed match explanations</li>
                    <li>• User can override suggestions</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Agent 3: Rating Calculator */}
            <div className="p-8 rounded-lg border bg-card shadow-sm">
              <div className="flex items-start gap-4 mb-4">
                <div className="p-3 rounded-lg bg-amber-100 dark:bg-amber-900">
                  <Scale className="h-6 w-6 text-amber-600 dark:text-amber-400" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">3. Rating Calculator Agent</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Computes objective sustainability scores based on verified criteria
                  </p>
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4 ml-16">
                <div>
                  <h4 className="font-medium text-sm mb-2 text-green-600 dark:text-green-400">✓ Compliance Measures:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Evidence-based scoring criteria</li>
                    <li>• Certified standards (GOTS, Fair Trade)</li>
                    <li>• No greenwashing promotion</li>
                    <li>• Third-party verification required</li>
                    <li>• Transparent methodology published</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-sm mb-2 text-blue-600 dark:text-blue-400">⚙️ How It Works:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• 0-100 sustainability scale</li>
                    <li>• Material composition analysis</li>
                    <li>• Certification validation</li>
                    <li>• Carbon footprint estimation</li>
                    <li>• Supply chain transparency check</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Agent 4: Brand Data Collector */}
            <div className="p-8 rounded-lg border bg-card shadow-sm">
              <div className="flex items-start gap-4 mb-4">
                <div className="p-3 rounded-lg bg-green-100 dark:bg-green-900">
                  <FileCheck className="h-6 w-6 text-green-600 dark:text-green-400" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">4. Brand Data Collector Agent</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Ethically aggregates sustainable product data from verified sources
                  </p>
                </div>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4 ml-16">
                <div>
                  <h4 className="font-medium text-sm mb-2 text-green-600 dark:text-green-400">✓ Compliance Measures:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Respects robots.txt policies</li>
                    <li>• Rate limiting to avoid overload</li>
                    <li>• Terms of service compliance</li>
                    <li>• Only public data collection</li>
                    <li>• Attribution to original sources</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-medium text-sm mb-2 text-blue-600 dark:text-blue-400">⚙️ How It Works:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• 35+ verified sustainable brands</li>
                    <li>• Product data normalization</li>
                    <li>• Automatic updates (weekly)</li>
                    <li>• Quality validation checks</li>
                    <li>• Dead link removal</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Accountability */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8 flex items-center gap-2">
            <AlertCircle className="h-6 w-6 text-primary" />
            Accountability & Continuous Improvement
          </h2>
          
          <div className="p-8 rounded-lg border bg-card">
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <h3 className="font-semibold mb-3">Regular Audits</h3>
                <p className="text-sm text-muted-foreground">
                  Quarterly reviews of AI algorithms for bias, fairness, and accuracy by independent auditors.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-3">User Feedback</h3>
                <p className="text-sm text-muted-foreground">
                  Active feedback mechanisms allow users to report issues, incorrect recommendations, or concerns.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Open Source</h3>
                <p className="text-sm text-muted-foreground">
                  Core algorithms are open source on GitHub for community review and contributions.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Certifications */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold mb-8">Certifications & Standards</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="p-6 rounded-lg border bg-card">
              <h3 className="font-semibold mb-2">GDPR Compliant</h3>
              <p className="text-sm text-muted-foreground mb-3">
                Full compliance with EU General Data Protection Regulation for user privacy and data rights.
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="text-xs px-3 py-1 rounded-full bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300">
                  Article 6 - Lawful Processing
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300">
                  Article 7 - Consent
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300">
                  Article 17 - Right to Erasure
                </span>
              </div>
            </div>

            <div className="p-6 rounded-lg border bg-card">
              <h3 className="font-semibold mb-2">ISO/IEC 27001</h3>
              <p className="text-sm text-muted-foreground mb-3">
                Information security management standards for protecting user data and maintaining confidentiality.
              </p>
              <div className="flex flex-wrap gap-2">
                <span className="text-xs px-3 py-1 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
                  Data Encryption
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
                  Access Control
                </span>
                <span className="text-xs px-3 py-1 rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
                  Security Audits
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* Contact */}
        <section className="text-center p-8 rounded-lg border bg-gradient-to-br from-primary/5 to-primary/10">
          <h2 className="text-2xl font-bold mb-4">Questions or Concerns?</h2>
          <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
            We're committed to transparency and accountability. If you have questions about our AI practices or want to report a concern, please reach out.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <a 
              href="mailto:ai-ethics@stylesustain.com" 
              className="px-6 py-3 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition-colors font-medium"
            >
              Contact AI Ethics Team
            </a>
            <Link 
              href="https://github.com/shoppingPlanners/sustainable-shopping-planner" 
              className="px-6 py-3 rounded-lg border border-primary text-primary hover:bg-primary/10 transition-colors font-medium"
            >
              View on GitHub
            </Link>
          </div>
        </section>
      </main>
    </div>
  )
}


