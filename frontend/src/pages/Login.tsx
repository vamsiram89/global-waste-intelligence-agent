import { useNavigate } from "react-router-dom";
import { Facebook, Leaf, Mail, ShieldCheck, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

export default function Login() {
  const navigate = useNavigate();

  return (
    <div className="grid min-h-screen bg-white lg:grid-cols-[1.05fr_0.95fr]">
      <section className="flex items-center justify-center px-6 py-10">
        <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
          <div className="flex items-center gap-3">
            <div className="grid h-12 w-12 place-items-center rounded-2xl bg-navy text-white">
              <Leaf className="h-6 w-6" />
            </div>
            <div>
              <p className="text-lg font-black text-ink">Smart Food Safe</p>
              <p className="text-sm text-slate-500">Global waste intelligent agent</p>
            </div>
          </div>

          <div className="mt-12">
            <p className="text-sm font-bold text-leaf">Welcome back</p>
            <h1 className="mt-3 text-4xl font-black tracking-normal text-ink">Automate compliance. Ensure safety.</h1>
            <p className="mt-4 leading-7 text-slate-500">Predict expiry risk, prevent waste, and coordinate safe redistribution from one clean control room.</p>
          </div>

          <div className="mt-8 grid gap-3 sm:grid-cols-2">
            <button className="btn-secondary"><Mail className="h-4 w-4" /> Sign in with Google</button>
            <button className="btn-secondary"><Facebook className="h-4 w-4" /> Sign in with Facebook</button>
          </div>

          <form className="mt-7 space-y-5" onSubmit={(event) => { event.preventDefault(); navigate("/dashboard"); }}>
            <div>
              <label className="label" htmlFor="email">Email</label>
              <input id="email" type="email" className="field" placeholder="operator@smartfoodsafe.com" />
            </div>
            <div>
              <label className="label" htmlFor="password">Password</label>
              <input id="password" type="password" className="field" placeholder="••••••••" />
            </div>
            <button className="btn-primary w-full" type="submit">Login</button>
          </form>
        </motion.div>
      </section>

      <section className="relative hidden overflow-hidden bg-navy p-10 text-white lg:block">
        <div className="absolute inset-0 bg-[linear-gradient(135deg,rgba(30,158,103,0.35),transparent_45%),radial-gradient(circle_at_80%_20%,rgba(47,128,237,0.45),transparent_26rem)]" />
        <div className="relative z-10 flex h-full flex-col justify-between">
          <div className="ml-auto rounded-full bg-white/12 px-4 py-2 text-sm font-semibold">Hello User!</div>
          <div>
            <div className="mb-7 grid h-16 w-16 place-items-center rounded-3xl bg-white/12">
              <ShieldCheck className="h-8 w-8 text-mint" />
            </div>
            <h2 className="max-w-lg text-6xl font-black tracking-normal">Safety-first food intelligence.</h2>
            <p className="mt-6 max-w-md text-lg leading-8 text-blue-100">Built for restaurants, supermarkets, warehouses, delivery apps, NGOs, and recycling partners.</p>
          </div>
          <div className="grid grid-cols-3 gap-4">
            {["Expiry risk", "Human approval", "Partner matching"].map((item) => (
              <div key={item} className="rounded-2xl border border-white/15 bg-white/10 p-4 backdrop-blur">
                <Sparkles className="h-5 w-5 text-mint" />
                <p className="mt-3 text-sm font-bold">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
