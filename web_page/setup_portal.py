import os

BASE = os.path.join(os.path.dirname(__file__), "frontend")

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  + {path}")

print("Setting up PACS Test Portal frontend...")

w("package.json", """{
  "name": "pacs-portal",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev -p 3000",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "next": "^16.1.1",
    "framer-motion": "^12.23.2",
    "lucide-react": "^0.525.0",
    "sonner": "^2.0.6",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "tailwind-merge": "^3.3.1",
    "@radix-ui/react-slot": "^1.2.3",
    "@radix-ui/react-label": "^2.1.7",
    "@radix-ui/react-avatar": "^1.1.10",
    "@radix-ui/react-separator": "^1.1.7"
  },
  "devDependencies": {
    "@types/node": "^22",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "typescript": "^5",
    "eslint": "^9",
    "eslint-config-next": "^16.1.1",
    "@tailwindcss/postcss": "^4",
    "tailwindcss": "^4",
    "tw-animate-css": "^1.3.5"
  }
}
""")

w("tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "noImplicitAny": false,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
""")

w("next.config.ts", """import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: "http://127.0.0.1:5000/api/:path*" }];
  },
};
export default nextConfig;
""")

w("postcss.config.mjs", """const config = { plugins: ["@tailwindcss/postcss"] };
export default config;
""")

w(".gitignore", """node_modules
.next
.env
.env.local
*.tsbuildinfo
next-env.d.ts
""")

w("src/app/globals.css", """@import "tailwindcss";
@import "tw-animate-css";
@custom-variant dark (&:is(.dark *));
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --font-sans: var(--font-geist-sans);
  --font-mono: var(--font-geist-mono);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}
:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
}
@layer base {
  * { @apply border-border outline-ring/50; }
  body { @apply bg-background text-foreground; }
}
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background-color: oklch(0.8 0 0 / 40%); border-radius: 3px; }
""")

w("src/app/layout.tsx", """import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Toaster } from "sonner";
const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });
export const metadata: Metadata = {
  title: "PACS Test Automation Portal",
  description: "Test Automation Portal for RhythmERP Company Onboarding module.",
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased bg-background text-foreground`}>
        {children}
        <Toaster position="top-right" richColors closeButton />
      </body>
    </html>
  );
}
""")

w("src/app/page.tsx", """"use client";
import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { LoginView } from "@/components/login-view";
import { DashboardView } from "@/components/dashboard-view";
export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const user = localStorage.getItem("pacs_user");
    if (user) setIsLoggedIn(true);
    setLoading(false);
  }, []);
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-muted/30">
        <div className="size-6 border-2 border-primary/30 border-t-primary rounded-full animate-spin" />
      </div>
    );
  }
  return (
    <AnimatePresence mode="wait">
      {isLoggedIn ? (
        <motion.div key="dashboard" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.3 }}>
          <DashboardView onSignOut={() => setIsLoggedIn(false)} />
        </motion.div>
      ) : (
        <motion.div key="login" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={{ duration: 0.3 }}>
          <LoginView onLogin={() => setIsLoggedIn(true)} />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
""")

w("src/lib/utils.ts", """import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)); }
""")

w("src/components/ui/button.tsx", """import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow-xs hover:bg-primary/90",
        destructive: "bg-destructive text-white shadow-xs hover:bg-destructive/90",
        outline: "border bg-background shadow-xs hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-xs hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md gap-1.5 px-3",
        lg: "h-10 rounded-md px-6",
        icon: "size-9",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
);
function Button({ className, variant, size, asChild = false, ...props }: React.ComponentProps<"button"> & VariantProps<typeof buttonVariants> & { asChild?: boolean }) {
  const Comp = asChild ? Slot : "button";
  return <Comp data-slot="button" className={cn(buttonVariants({ variant, size, className }))} {...props} />;
}
export { Button, buttonVariants };
""")

w("src/components/ui/card.tsx", """import * as React from "react";
import { cn } from "@/lib/utils";
function Card({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="card" className={cn("bg-card text-card-foreground flex flex-col gap-6 rounded-xl border py-6 shadow-sm", className)} {...props} />;
}
function CardHeader({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="card-header" className={cn("grid auto-rows-min grid-rows-[auto_auto] items-start gap-1.5 px-6", className)} {...props} />;
}
function CardTitle({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="card-title" className={cn("leading-none font-semibold", className)} {...props} />;
}
function CardDescription({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="card-description" className={cn("text-muted-foreground text-sm", className)} {...props} />;
}
function CardContent({ className, ...props }: React.ComponentProps<"div">) {
  return <div data-slot="card-content" className={cn("px-6", className)} {...props} />;
}
export { Card, CardHeader, CardTitle, CardDescription, CardContent };
""")

w("src/components/ui/input.tsx", """import * as React from "react";
import { cn } from "@/lib/utils";
function Input({ className, type, ...props }: React.ComponentProps<"input">) {
  return (
    <input type={type} data-slot="input"
      className={cn("file:text-foreground placeholder:text-muted-foreground border-input flex h-9 w-full min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-colors outline-none disabled:pointer-events-none disabled:opacity-50 md:text-sm", "focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px]", className)}
      {...props} />
  );
}
export { Input };
""")

w("src/components/ui/label.tsx", """"use client";
import * as React from "react";
import * as LabelPrimitive from "@radix-ui/react-label";
import { cn } from "@/lib/utils";
function Label({ className, ...props }: React.ComponentProps<typeof LabelPrimitive.Root>) {
  return <LabelPrimitive.Root data-slot="label" className={cn("flex items-center gap-2 text-sm leading-none font-medium select-none", className)} {...props} />;
}
export { Label };
""")

w("src/components/ui/badge.tsx", """import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
const badgeVariants = cva(
  "inline-flex items-center justify-center rounded-md border px-2 py-0.5 text-xs font-medium w-fit whitespace-nowrap shrink-0 transition-colors",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground",
        secondary: "border-transparent bg-secondary text-secondary-foreground",
        destructive: "border-transparent bg-destructive text-white",
        outline: "text-foreground",
      },
    },
    defaultVariants: { variant: "default" },
  }
);
function Badge({ className, variant, asChild = false, ...props }: React.ComponentProps<"span"> & VariantProps<typeof badgeVariants> & { asChild?: boolean }) {
  const Comp = asChild ? Slot : "span";
  return <Comp data-slot="badge" className={cn(badgeVariants({ variant }), className)} {...props} />;
}
export { Badge, badgeVariants };
""")

w("src/components/ui/avatar.tsx", """"use client";
import * as React from "react";
import * as AvatarPrimitive from "@radix-ui/react-avatar";
import { cn } from "@/lib/utils";
function Avatar({ className, ...props }: React.ComponentProps<typeof AvatarPrimitive.Root>) {
  return <AvatarPrimitive.Root data-slot="avatar" className={cn("relative flex size-8 shrink-0 overflow-hidden rounded-full", className)} {...props} />;
}
function AvatarFallback({ className, ...props }: React.ComponentProps<typeof AvatarPrimitive.Fallback>) {
  return <AvatarPrimitive.Fallback data-slot="avatar-fallback" className={cn("bg-muted flex size-full items-center justify-center rounded-full", className)} {...props} />;
}
export { Avatar, AvatarFallback };
""")

w("src/components/ui/separator.tsx", """"use client";
import * as React from "react";
import * as SeparatorPrimitive from "@radix-ui/react-separator";
import { cn } from "@/lib/utils";
function Separator({ className, orientation = "horizontal", decorative = true, ...props }: React.ComponentProps<typeof SeparatorPrimitive.Root>) {
  return <SeparatorPrimitive.Root data-slot="separator" decorative={decorative} orientation={orientation} className={cn("bg-border shrink-0 data-[orientation=horizontal]:h-px data-[orientation=horizontal]:w-full data-[orientation=vertical]:h-full data-[orientation=vertical]:w-px", className)} {...props} />;
}
export { Separator };
""")

w("src/components/ui/table.tsx", """"use client";
import * as React from "react";
import { cn } from "@/lib/utils";
function Table({ className, ...props }: React.ComponentProps<"table">) {
  return <div data-slot="table-container" className="relative w-full overflow-x-auto"><table data-slot="table" className={cn("w-full caption-bottom text-sm", className)} {...props} /></div>;
}
function TableHeader({ className, ...props }: React.ComponentProps<"thead">) {
  return <thead data-slot="table-header" className={cn("[&_tr]:border-b", className)} {...props} />;
}
function TableBody({ className, ...props }: React.ComponentProps<"tbody">) {
  return <tbody data-slot="table-body" className={cn("[&_tr:last-child]:border-0", className)} {...props} />;
}
function TableRow({ className, ...props }: React.ComponentProps<"tr">) {
  return <tr data-slot="table-row" className={cn("hover:bg-muted/50 data-[state=selected]:bg-muted border-b transition-colors", className)} {...props} />;
}
function TableHead({ className, ...props }: React.ComponentProps<"th">) {
  return <th data-slot="table-head" className={cn("text-foreground h-10 px-2 text-left align-middle font-medium whitespace-nowrap", className)} {...props} />;
}
function TableCell({ className, ...props }: React.ComponentProps<"td">) {
  return <td data-slot="table-cell" className={cn("p-2 align-middle whitespace-nowrap", className)} {...props} />;
}
export { Table, TableHeader, TableBody, TableRow, TableHead, TableCell };
""")

# LOGIN VIEW - connected to real Flask API
w("src/components/login-view.tsx", """"use client";
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
""")

# DASHBOARD VIEW - connected to real Flask API
w("src/components/dashboard-view.tsx", """"use client";
import { useEffect, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { FlaskConical, CheckCircle2, XCircle, Clock, Plus, RefreshCw, Play, FileText, FileSpreadsheet, BarChart3, LogOut, Eye, Download, X, Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Separator } from "@/components/ui/separator";
interface Stats { total: number; passed: number; failed: number; running: number; avg_duration: number; pass_rate: number; }
interface TestRun { id: number; test_type: string; status: string; duration_seconds: number | null; started_at: string; finished_at: string | null; }
interface Report { filename: string; size: number; modified: number; type: string; }
interface DashboardViewProps { onSignOut: () => void; }
const fadeInUp = { initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.4, ease: "easeOut" as const } };
const stagger = { animate: { transition: { staggerChildren: 0.07 } } };
function fmtDur(s: number | null) { if (!s) return "-"; const m = Math.floor(s / 60); const sec = Math.round(s % 60); return m > 0 ? m + "m " + sec + "s" : sec + "s"; }
function fmtSize(b: number) { if (b < 1024) return b + " B"; if (b < 1048576) return (b / 1024).toFixed(1) + " KB"; return (b / 1048576).toFixed(1) + " MB"; }
function fmtDate(d: string) { return new Date(d).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
export function DashboardView({ onSignOut }: DashboardViewProps) {
  const [stats, setStats] = useState<Stats>({ total: 0, passed: 0, failed: 0, running: 0, avg_duration: 0, pass_rate: 0 });
  const [runs, setRuns] = useState<TestRun[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [user, setUser] = useState<{ displayName: string; username: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [selectedTest, setSelectedTest] = useState("creation");
  const [companyCount, setCompanyCount] = useState(1);
  const loadData = useCallback(async () => {
    try {
      const [s, r, rp] = await Promise.all([fetch("/api/stats"), fetch("/api/runs"), fetch("/api/reports")]);
      setStats(await s.json());
      setRuns(await r.json());
      setReports(await rp.json());
    } catch (e) { console.error(e); }
  }, []);
  useEffect(() => {
    const stored = localStorage.getItem("pacs_user");
    if (!stored) { onSignOut(); return; }
    setUser(JSON.parse(stored));
    loadData();
    const iv = setInterval(loadData, 5000);
    return () => clearInterval(iv);
  }, [loadData, onSignOut]);
  async function handleRun() {
    setLoading(true); setShowModal(false);
    try {
      const res = await fetch("/api/runs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ testType: selectedTest, companyCount }) });
      const data = await res.json();
      if (data.success) { toast.success(data.message); setTimeout(loadData, 2000); } else { toast.error(data.error || "Failed"); }
    } catch { toast.error("Failed to start test"); } finally { setLoading(false); }
  }
  const cards = [
    { title: "Total Tests", value: String(stats.total), sub: stats.running + " running", icon: FlaskConical, ic: "text-primary", ib: "bg-primary/10" },
    { title: "Passed", value: String(stats.passed), sub: stats.pass_rate + "% rate", icon: CheckCircle2, ic: "text-emerald-600", ib: "bg-emerald-50" },
    { title: "Failed", value: String(stats.failed), sub: "Needs attention", icon: XCircle, ic: "text-red-600", ib: "bg-red-50" },
    { title: "Avg Duration", value: fmtDur(stats.avg_duration), sub: "Per test", icon: Clock, ic: "text-amber-600", ib: "bg-amber-50" },
  ];
  const actions = [
    { label: "Run Creation Test", sub: "Create new company records", icon: Plus, v: "bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm shadow-emerald-600/25" },
    { label: "Run Update Test", sub: "Update existing company data", icon: RefreshCw, v: "bg-amber-600 hover:bg-amber-700 text-white shadow-sm shadow-amber-600/25" },
    { label: "Run Full Suite", sub: "Complete end-to-end test", icon: Play, v: "" },
  ];
  const initials = user?.displayName?.split(" ").map((n: string) => n[0]).join("").toUpperCase() || "U";
  return (
    <div className="min-h-screen flex flex-col bg-muted/30">
      <motion.header initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }} className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur">
        <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center size-9 rounded-xl bg-primary text-primary-foreground font-bold text-sm shadow-sm"><FlaskConical className="size-5" /></div>
            <div className="flex flex-col"><span className="text-sm font-bold text-foreground leading-none">PACS</span><span className="text-xs text-muted-foreground leading-none mt-0.5">Test Automation Portal</span></div>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2.5">
              <Avatar className="size-8"><AvatarFallback className="bg-primary/10 text-primary text-xs font-semibold">{initials}</AvatarFallback></Avatar>
              <span className="text-sm font-medium text-foreground">{user?.displayName || "User"}</span>
            </div>
            <Separator orientation="vertical" className="hidden sm:block h-6" />
            <Button variant="ghost" size="sm" onClick={onSignOut} className="text-muted-foreground hover:text-foreground gap-1.5"><LogOut className="size-4" /><span className="hidden sm:inline">Sign Out</span></Button>
          </div>
        </div>
      </motion.header>
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-8">
        <motion.div variants={stagger} initial="initial" animate="animate" className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
          {cards.map((c) => { const Icon = c.icon; return (
            <motion.div key={c.title} variants={fadeInUp}>
              <Card className="hover:shadow-md transition-shadow duration-200">
                <CardContent className="p-5">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <p className="text-sm font-medium text-muted-foreground">{c.title}</p>
                      <p className="text-3xl font-bold tracking-tight text-foreground">{c.value}</p>
                      <p className="text-xs text-muted-foreground">{c.sub}</p>
                    </div>
                    <div className={"size-10 rounded-xl flex items-center justify-center " + c.ib}><Icon className={"size-5 " + c.ic} /></div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ); })}
        </motion.div>
        <motion.div {...fadeInUp} transition={{ duration: 0.4, delay: 0.28 }}>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Quick Actions</CardTitle>
              <CardDescription>Launch a test run for the Company Onboarding module</CardDescription>
            </CardHeader>
            <CardContent className="pt-2">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {actions.map((a) => { const Icon = a.icon; const isCustom = a.v !== ""; return (
                  <button key={a.label} onClick={() => { setSelectedTest(a.label.toLowerCase().includes("creation") ? "creation" : a.label.toLowerCase().includes("update") ? "update" : "full"); setShowModal(true); }}
                    className={"group flex flex-col items-start gap-2 rounded-xl border p-4 text-left transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 " + (isCustom ? a.v + " border-transparent" : "bg-primary hover:bg-primary/90 text-primary-foreground border-primary shadow-sm shadow-primary/25")}>
                    <div className="flex items-center gap-2 w-full">
                      <div className="flex items-center justify-center size-8 rounded-lg bg-white/20"><Icon className="size-4" /></div>
                      <span className="text-sm font-semibold">{a.label}</span>
                    </div>
                    <p className={"text-xs leading-relaxed " + (isCustom ? "text-white/80" : "text-primary-foreground/80")}>{a.sub}</p>
                  </button>
                ); })}
              </div>
            </CardContent>
          </Card>
        </motion.div>
        <motion.div {...fadeInUp} transition={{ duration: 0.4, delay: 0.36 }}>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Recent Test Runs</CardTitle>
              <CardDescription>Latest automation results for Company Onboarding</CardDescription>
            </CardHeader>
            <CardContent className="pt-2">
              <div className="max-h-96 overflow-y-auto custom-scrollbar">
                <Table>
                  <TableHeader>
                    <TableRow className="hover:bg-transparent">
                      <TableHead className="w-12 text-xs font-semibold">#</TableHead>
                      <TableHead className="text-xs font-semibold">Test Type</TableHead>
                      <TableHead className="text-xs font-semibold">Status</TableHead>
                      <TableHead className="text-xs font-semibold">Duration</TableHead>
                      <TableHead className="text-xs font-semibold">Started</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {runs.length === 0 ? (
                      <TableRow><TableCell colSpan={5} className="text-center text-muted-foreground py-8">No test runs yet. Click a button above to start!</TableCell></TableRow>
                    ) : runs.slice(0, 20).map((r) => (
                      <TableRow key={r.id}>
                        <TableCell className="text-muted-foreground font-mono text-xs">{r.id}</TableCell>
                        <TableCell className="font-medium text-sm">{r.test_type.charAt(0).toUpperCase() + r.test_type.slice(1)}</TableCell>
                        <TableCell>
                          <Badge variant={r.status === "PASSED" ? "default" : r.status === "FAILED" ? "destructive" : "secondary"} className={r.status === "PASSED" ? "bg-emerald-100 text-emerald-700 border-emerald-200" : r.status === "RUNNING" ? "bg-blue-100 text-blue-700 border-blue-200" : ""}>{r.status}</Badge>
                        </TableCell>
                        <TableCell className="text-sm text-muted-foreground font-mono">{fmtDur(r.duration_seconds)}</TableCell>
                        <TableCell className="text-sm text-muted-foreground">{fmtDate(r.started_at)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </motion.div>
        <motion.div {...fadeInUp} transition={{ duration: 0.4, delay: 0.44 }}>
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-foreground">Latest Reports</h2>
            <p className="text-sm text-muted-foreground">Generated test execution reports</p>
          </div>
          {reports.length === 0 ? (
            <Card><CardContent className="py-8 text-center text-muted-foreground">No reports generated yet.</CardContent></Card>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
              {reports.slice(0, 10).map((rp) => {
                const Icon = rp.type === "Update" ? FileSpreadsheet : rp.filename.includes("Bulk") ? BarChart3 : FileText;
                return (
                  <motion.div key={rp.filename} variants={fadeInUp}>
                    <Card className="hover:shadow-md transition-shadow duration-200">
                      <CardContent className="p-5">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex items-center gap-3">
                            <div className="size-10 rounded-xl bg-primary/10 flex items-center justify-center"><Icon className="size-5 text-primary" /></div>
                            <div>
                              <h3 className="text-sm font-semibold text-foreground">{rp.filename}</h3>
                              <p className="text-xs text-muted-foreground">{rp.type} · {fmtSize(rp.size)}</p>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center justify-between mt-4 pt-3 border-t">
                          <span className="text-xs text-muted-foreground">{fmtDate(new Date(rp.modified * 1000).toISOString())}</span>
                          <a href={"/api/reports/" + encodeURIComponent(rp.filename)} className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:text-primary/80"><Download className="size-3.5" />Download</a>
                        </div>
                      </CardContent>
                    </Card>
                  </motion.div>
                );
              })}
            </div>
          )}
        </motion.div>
      </main>
      <motion.footer initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.4, delay: 0.5 }} className="border-t bg-background mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-center">
          <p className="text-xs text-muted-foreground">PACS Automation Portal · v1.0 · 2026</p>
        </div>
      </motion.footer>
      <AnimatePresence>
        {showModal && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
            <motion.div initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.95, opacity: 0 }}>
              <Card className="w-full max-w-sm">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Run {selectedTest.charAt(0).toUpperCase() + selectedTest.slice(1)} Test</h3>
                    <button onClick={() => setShowModal(false)} className="text-muted-foreground hover:text-foreground"><X className="size-4" /></button>
                  </div>
                  {selectedTest === "creation" && (
                    <div className="mb-4">
                      <label className="text-sm font-medium mb-2 block">Number of Companies</label>
                      <select value={companyCount} onChange={(e) => setCompanyCount(Number(e.target.value))} className="w-full h-9 rounded-md border border-input bg-transparent px-3 text-sm">
                        {[1, 2, 3, 5, 10, 20].map((n) => <option key={n} value={n}>{n}</option>)}
                      </select>
                    </div>
                  )}
                  <p className="text-sm text-muted-foreground mb-4">This will start the test in the background. Results will appear in the test history.</p>
                  <div className="flex gap-3 justify-end">
                    <Button variant="outline" size="sm" onClick={() => setShowModal(false)}>Cancel</Button>
                    <Button size="sm" onClick={handleRun} disabled={loading}>{loading ? <Loader2 className="size-4 animate-spin" /> : null}{loading ? "Starting..." : "Start Test"}</Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
""")

print()
print("All files created!")
print("Next steps:")
print("  cd frontend")
print("  npm install")
print("  npm run dev")
print("  Open http://localhost:3000")