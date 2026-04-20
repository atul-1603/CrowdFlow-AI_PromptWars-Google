"use client";

import React from "react";
import Link from "next/link";
import {
  ArrowRight,
  Map as MapIcon,
  Cpu,
  Navigation as NavIcon,
  ShieldCheck,
  BarChart3,
  Zap,
  ChevronRight
} from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

export default function LandingPage() {
  const { isAuthenticated } = useAuth();
  return (
    <div className="bg-background text-foreground selection:bg-primary/30">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-background/50 backdrop-blur-xl border-b border-white/5">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-tr from-primary to-accent rounded-xl flex items-center justify-center text-primary-foreground font-bold text-xl shadow-lg shadow-primary/20">
              C
            </div>
            <span className="text-xl font-black tracking-tighter">CROWDFLOW AI</span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
            <a href="#features" className="hover:text-primary transition-colors">Features</a>
            <a href="#demo" className="hover:text-primary transition-colors">Demo</a>
            <a href="#how-it-works" className="hover:text-primary transition-colors">Solutions</a>
          </div>
          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <Link href="/dashboard" className="text-sm font-bold px-6 py-2.5 bg-primary text-primary-foreground rounded-xl shadow-lg shadow-primary/20 hover:scale-105 active:scale-95 transition-all">
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link href="/login" className="text-sm font-bold px-5 py-2.5 rounded-xl hover:bg-secondary transition-all">Log In</Link>
                <Link href="/signup" className="text-sm font-bold px-6 py-2.5 bg-primary text-primary-foreground rounded-xl shadow-lg shadow-primary/20 hover:scale-105 active:scale-95 transition-all">
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center pt-20 overflow-hidden">
        <div className="absolute inset-0 z-0">
          <img 
            src="/images/hero.png" 
            alt="Stadium Hero" 
            className="w-full h-full object-cover opacity-40 mix-blend-luminosity"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background via-background/80 to-background"></div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8 animate-in slide-in-from-left duration-1000">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold uppercase tracking-widest">
              <Zap size={14} /> Next Gen Stadium Intelligence
            </div>
            <h1 className="text-6xl md:text-8xl font-black tracking-tight leading-[0.9]">
              OPTIMIZE <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary via-accent to-primary animate-gradient-x">THE FLOW.</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-lg leading-relaxed">
              CrowdFlow AI transforms stadium chaos into intelligent precision. Real-time tracking, predictive routing, and AI assistance for the ultimate fan experience.
            </p>
            <div className="flex flex-col sm:flex-row items-center gap-4 pt-4">
              <Link href="/signup" className="w-full sm:w-auto px-8 py-4 bg-primary text-primary-foreground font-black rounded-2xl shadow-xl shadow-primary/30 hover:-translate-y-1 transition-all flex items-center justify-center gap-2 text-lg">
                Deploy System <ArrowRight size={20} />
              </Link>
              <a href="#demo" className="w-full sm:w-auto px-8 py-4 bg-secondary border border-white/5 font-bold rounded-2xl hover:bg-secondary/80 transition-all text-center">
                Watch Demo
              </a>
            </div>
          </div>
          <div className="hidden lg:block relative animate-in zoom-in duration-1000 delay-300">
            <div className="absolute -inset-4 bg-gradient-to-tr from-primary to-accent opacity-20 blur-3xl animate-pulse"></div>
            <img 
              src="/images/mockup.png" 
              alt="Dashboard Preview" 
              className="relative rounded-3xl border border-white/10 shadow-2xl shadow-black/50 rotate-2 hover:rotate-0 transition-all duration-700"
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-32 relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center space-y-4 mb-20">
            <h2 className="text-4xl md:text-5xl font-black">POWERING EVERY MOVE.</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our proprietary multi-modal AI engine processes millions of data points to ensure your venue operates at peak efficiency.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={<MapIcon className="text-primary" />}
              title="Real-Time Tracking"
              description="Monitor crowd density across your entire venue with meter-level precision using IoT and sensor fusion."
            />
            <FeatureCard 
              icon={<Cpu className="text-accent" />}
              title="AI Decision Engine"
              description="Vertex AI powered agents provide actionable insights and automated responses to congestion events."
            />
            <FeatureCard 
              icon={<NavIcon className="text-success" />}
              title="Predictive Routing"
              description="Guide fans to the shortest queues and safest paths automatically via dynamic signage and mobile apps."
            />
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section id="demo" className="py-32 bg-secondary/30 relative">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
          <div className="relative order-2 lg:order-1">
            <img 
              src="/images/feature.png" 
              alt="Live Analysis" 
              className="rounded-3xl border border-white/5 shadow-2xl"
            />
            <div className="absolute -bottom-10 -right-10 p-6 bg-background/80 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl hidden md:block">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-success/20 rounded-full flex items-center justify-center text-success">
                  <BarChart3 size={24} />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground uppercase font-black">Optimization</p>
                  <p className="text-xl font-bold">+24% Efficiency</p>
                </div>
              </div>
            </div>
          </div>
          <div className="space-y-8 order-1 lg:order-2">
            <h2 className="text-4xl md:text-5xl font-black leading-tight">
              A COMMAND CENTER <br />
              FOR THE FUTURE.
            </h2>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Don't just react to crowds—orchestrate them. Our unified dashboard gives you a god-mode view of your stadium, allowing you to prevent bottlenecks before they happen.
            </p>
            <ul className="space-y-4">
              <li className="flex items-center gap-3 font-bold">
                <ShieldCheck className="text-primary" /> Enterprise-grade Security
              </li>
              <li className="flex items-center gap-3 font-bold">
                <ShieldCheck className="text-primary" /> Sub-second Latency
              </li>
              <li className="flex items-center gap-3 font-bold">
                <ShieldCheck className="text-primary" /> Scalable to Millions
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-32">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h2 className="text-4xl font-black mb-20">THE INTELLIGENCE LOOP.</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 relative">
            <Step number="01" title="INGEST" desc="IoT sensors capture real-time movement." />
            <Step number="02" title="ANALYZE" desc="AI identifies patterns and risks." />
            <Step number="03" title="ACT" desc="Automated routing guides the flow." />
            <Step number="04" title="OPTIMIZE" desc="Fans enjoy a frictionless experience." />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32">
        <div className="max-w-5xl mx-auto px-6">
          <div className="p-12 md:p-20 rounded-[3rem] bg-gradient-to-tr from-primary to-accent relative overflow-hidden text-center space-y-8">
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-20"></div>
            <h2 className="text-4xl md:text-6xl font-black text-primary-foreground leading-none relative z-10">
              READY TO REVOLUTIONIZE <br /> YOUR VENUE?
            </h2>
            <p className="text-primary-foreground/80 text-lg max-w-xl mx-auto relative z-10">
              Join leading stadiums worldwide using CrowdFlow AI to power their operations.
            </p>
            <div className="relative z-10 pt-4">
              <Link href="/signup" className="px-10 py-5 bg-background text-foreground font-black rounded-2xl shadow-2xl hover:scale-105 active:scale-95 transition-all inline-flex items-center gap-3">
                Start Your Trial <ArrowRight />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-20 border-t border-white/5">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-12">
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-primary-foreground font-bold">C</div>
              <span className="text-lg font-black tracking-tighter">CROWDFLOW AI</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Intelligent Stadium Management Systems. Built for the next billion fans.
            </p>
          </div>
          <div>
            <h4 className="font-bold mb-6">Product</h4>
            <ul className="space-y-4 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">Analytics</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">AI Routing</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Sensor Integration</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-6">Company</h4>
            <ul className="space-y-4 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Partners</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Contact</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-6">Legal</h4>
            <ul className="space-y-4 text-sm text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">Privacy Policy</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Terms of Service</a></li>
            </ul>
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-6 pt-12 mt-12 border-t border-white/5 text-center text-xs text-muted-foreground">
          &copy; 2026 CrowdFlow AI Technologies Inc. All rights reserved.
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactElement, title: string, description: string }) {
  return (
    <div className="p-8 rounded-3xl bg-secondary/20 border border-white/5 hover:border-primary/50 transition-all group hover:-translate-y-2 duration-500">
      <div className="w-14 h-14 bg-background rounded-2xl flex items-center justify-center mb-6 shadow-xl group-hover:scale-110 transition-transform">
        {React.cloneElement(icon, { size: 28 } as any)}
      </div>
      <h3 className="text-xl font-bold mb-4">{title}</h3>
      <p className="text-muted-foreground leading-relaxed">{description}</p>
      <div className="mt-8 flex items-center gap-2 text-primary text-sm font-bold opacity-0 group-hover:opacity-100 transition-opacity">
        Learn more <ChevronRight size={16} />
      </div>
    </div>
  );
}

function Step({ number, title, desc }: { number: string, title: string, desc: string }) {
  return (
    <div className="p-8 relative">
      <div className="text-5xl font-black text-primary/10 mb-4">{number}</div>
      <h4 className="text-lg font-bold mb-2">{title}</h4>
      <p className="text-sm text-muted-foreground">{desc}</p>
    </div>
  );
}
