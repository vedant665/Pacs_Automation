"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { FlaskConical, Lock, Mail, ArrowRight } from "lucide-react";
import { toast } from "sonner";
interface LoginViewProps { onLogin: () => void; }
export function LoginView({ onLogin }: LoginViewProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: email, password }),
      });
      const data = await res.json();
      if (data.success) {
        localStorage.setItem("pacs_user", JSON.stringify(data.user));
        onLogin();
      } else {
        toast.error(data.error || "Login failed");
      }
    } catch {
      toast.error("Cannot connect to server. Is Flask running?");
    } finally {
      setIsLoading(false);
    }
  };
  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
      </div>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, ease: "easeOut" }} className="w-full max-w-md relative z-10">
        <Card className="border-0 shadow-xl shadow-black/5">
          <CardContent className="p-8">
            <div className="flex flex-col items-center text-center mb-8">
              <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.4, delay: 0.1 }} className="w-16 h-16 rounded-2xl bg-primary flex items-center justify-center mb-4 shadow-lg shadow-primary/25">
                <FlaskConical className="w-8 h-8 text-primary-foreground" />
              </motion.div>
              <h1 className="text-2xl font-bold tracking-tight text-foreground">PACS</h1>
              <div className="mt-1 space-y-0.5">
                <p className="text-lg font-semibold text-foreground">Test Automation Portal</p>
                <p className="text-sm text-muted-foreground">RhythmERP Company Onboarding</p>
              </div>
            </div>
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-sm font-medium">Username</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
                  <Input id="email" type="text" placeholder="admin" value={email} onChange={(e) => setEmail(e.target.value)} className="pl-10 h-11" required />
                </div>
              </div>
              <div className="space-y-2">
                <Label htmlFor="password" className="text-sm font-medium">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-muted-foreground" />
                  <Input id="password" type="password" placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} className="pl-10 h-11" required />
                </div>
              </div>
              <Button type="submit" className="w-full h-11 text-sm font-semibold" disabled={isLoading}>
                {isLoading ? (
                  <div className="flex items-center gap-2"><div className="size-4 border-2 border-primary-foreground/30 border-t-primary-foreground rounded-full animate-spin" />Signing in...</div>
                ) : (
                  <div className="flex items-center gap-2">Sign In<ArrowRight className="size-4" /></div>
                )}
              </Button>
            </form>
            <p className="text-xs text-center text-muted-foreground mt-6">Default: admin / admin123</p>
          </CardContent>
        </Card>
        <p className="text-xs text-center text-muted-foreground/60 mt-6">PACS Automation Portal · v1.0 · 2026</p>
      </motion.div>
    </div>
  );
}
