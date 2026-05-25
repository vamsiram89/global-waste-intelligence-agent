import { useState } from "react";
import { ExternalLink, RefreshCw, ShieldAlert } from "lucide-react";
import { API_BASE_URL, getFriendlyApiError, getHealth } from "../api/apiClient";
import ErrorMessage from "../components/ErrorMessage";
import GlassCard from "../components/GlassCard";
import RiskBadge from "../components/RiskBadge";

export default function Settings() {
  const [health, setHealth] = useState("Not checked");
  const [error, setError] = useState("");

  const refresh = async () => {
    setError("");
    try {
      const result = await getHealth();
      setHealth(result.status === "ok" ? "Online" : "Degraded");
    } catch (err) {
      setHealth("Offline");
      setError(getFriendlyApiError(err).message);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="font-semibold text-leaf">Configuration</p>
        <h1 className="text-3xl font-black tracking-normal text-ink">Settings</h1>
      </div>
      {error ? <ErrorMessage message={error} onRetry={refresh} /> : null}
      <div className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
        <GlassCard className="p-6">
          <h2 className="text-xl font-black text-ink">Backend Connection</h2>
          <div className="mt-5 rounded-2xl bg-slate-50 p-5">
            <p className="text-xs font-bold uppercase tracking-wide text-slate-400">API Base URL</p>
            <p className="mt-2 break-all text-lg font-black text-ink">{API_BASE_URL}</p>
          </div>
          <div className="mt-5 flex flex-wrap items-center gap-3">
            <RiskBadge level={health === "Online" ? "Safe" : health === "Offline" ? "Critical" : "Recommended"} />
            <button className="btn-secondary" onClick={refresh}><RefreshCw className="h-4 w-4" /> Refresh health</button>
            <a className="btn-primary" href="http://localhost:8000/docs" target="_blank" rel="noreferrer"><ExternalLink className="h-4 w-4" /> Swagger Docs</a>
          </div>
        </GlassCard>
        <GlassCard className="p-6">
          <h2 className="text-xl font-black text-ink">Future Enhancements</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {["POS and ERP integrations", "Real weather APIs", "Local event APIs", "Historical sales forecasting", "Route optimization", "Packaging supplier scorecards", "Multi-tenant authentication", "Human approval workflow", "Compliance audit exports"].map((item) => (
              <div key={item} className="rounded-2xl bg-slate-50 p-4 text-sm font-semibold text-slate-700">{item}</div>
            ))}
          </div>
        </GlassCard>
      </div>
      <div className="flex items-start gap-3 rounded-2xl border border-amber-100 bg-amber-50 p-5 text-sm leading-6 text-amber-900">
        <ShieldAlert className="mt-0.5 h-5 w-5 flex-none" />
        <p>This MVP is a decision-support prototype. Real deployment must include food safety validation, local legal compliance, cold-chain checks, expiry verification, partner approval, and human confirmation before redistribution or pickup. Never donate expired food.</p>
      </div>
    </div>
  );
}
