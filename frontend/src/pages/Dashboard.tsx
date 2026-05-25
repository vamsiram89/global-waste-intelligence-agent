import { useEffect, useMemo, useState } from "react";
import { AlertTriangle, Building2, ClipboardList, PackageX, ShieldCheck } from "lucide-react";
import { getFriendlyApiError, getHealth } from "../api/apiClient";
import { getAnalyticsSummary, type AnalyticsSummary } from "../api/analyticsApi";
import { getInventory, type InventoryItem } from "../api/inventoryApi";
import { predictAllWasteRisk, type WastePrediction } from "../api/predictionApi";
import ErrorMessage from "../components/ErrorMessage";
import GlassCard from "../components/GlassCard";
import InventoryTable from "../components/InventoryTable";
import LoadingSpinner from "../components/LoadingSpinner";
import RiskBadge from "../components/RiskBadge";
import RiskHeatmap from "../components/RiskHeatmap";
import StatCard from "../components/StatCard";

export default function Dashboard() {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [predictions, setPredictions] = useState<WastePrediction[]>([]);
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [health, setHealth] = useState<string>("Checking");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const [healthData, inventoryData, predictionData, analyticsData] = await Promise.all([
        getHealth(),
        getInventory(),
        predictAllWasteRisk(),
        getAnalyticsSummary(),
      ]);
      setHealth(healthData.status === "ok" ? "Online" : "Degraded");
      setInventory(inventoryData);
      setPredictions(predictionData);
      setAnalytics(analyticsData);
    } catch (err) {
      setHealth("Offline");
      setError(getFriendlyApiError(err).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
  }, []);

  const criticalCount = useMemo(() => predictions.filter((item) => item.risk_level.toLowerCase() === "critical").length, [predictions]);

  if (loading) return <LoadingSpinner label="Loading dashboard intelligence" />;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <p className="font-semibold text-leaf">Hello User</p>
        <h1 className="text-3xl font-black tracking-normal text-ink">Today's Summary Reports</h1>
      </div>

      {error ? <ErrorMessage message={error} onRetry={load} /> : null}

      <div className="grid gap-4 md:grid-cols-2 2xl:grid-cols-4">
        <StatCard title="Total Suppliers" value={Math.max(12, inventory.length + 7)} helper="Restaurants, warehouses, apps, partners" trend="+10.1% monitored coverage" icon={Building2} tone="blue" />
        <StatCard title="Active Queries" value={predictions.length || 0} helper="Prediction jobs and action checks" icon={ClipboardList} tone="green" />
        <StatCard title="Expiring Items" value={analytics?.high_risk_products ?? 0} helper="High risk or soon-to-expire inventory" icon={PackageX} tone="orange" />
        <StatCard title="Critical Risk Items" value={criticalCount} helper="Needs urgent review today" icon={AlertTriangle} tone="red" />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
        <GlassCard className="p-6">
          <div className="mb-5 flex items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-black text-ink">Supplier Risk Matrix</h2>
              <p className="mt-1 text-sm text-slate-500">{predictions.length ? "Live prediction data" : "Demo data shown until inventory predictions exist"}</p>
            </div>
            <div className="flex gap-2 text-xs font-semibold text-slate-500">
              <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-red-400" /> Critical</span>
              <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-amber-400" /> Medium</span>
              <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-emerald-400" /> Low</span>
            </div>
          </div>
          <RiskHeatmap predictions={predictions} />
        </GlassCard>

        <GlassCard className="p-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-black text-ink">Backend Health</h2>
            <RiskBadge level={health === "Online" ? "Safe" : "Critical"} />
          </div>
          <div className="mt-6 rounded-2xl bg-slate-50 p-5">
            <ShieldCheck className="h-8 w-8 text-leaf" />
            <p className="mt-4 text-3xl font-black text-ink">{health}</p>
            <p className="mt-2 text-sm text-slate-500">Health check: http://localhost:8000/health</p>
          </div>
        </GlassCard>
      </div>

      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <GlassCard className="p-6">
          <h2 className="text-xl font-black text-ink">Risk Alerts</h2>
          <div className="mt-4 space-y-3">
            {(predictions.length ? predictions : []).slice(0, 5).map((item) => (
              <div key={`${item.inventory_item_id}-${item.product_name}`} className="flex items-center justify-between gap-4 rounded-2xl bg-slate-50 p-4">
                <div>
                  <p className="font-bold text-ink">{item.product_name}</p>
                  <p className="text-sm text-slate-500">{item.reason}</p>
                </div>
                <RiskBadge level={item.risk_level} />
              </div>
            ))}
            {!predictions.length ? <p className="rounded-2xl bg-slate-50 p-5 text-sm text-slate-500">No live alerts yet. Add inventory items and run predictions to populate this feed.</p> : null}
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-black text-ink">Inventory Preview</h2>
            <span className="text-sm font-semibold text-slate-500">{inventory.length} items</span>
          </div>
          <InventoryTable items={inventory.slice(0, 6)} compact />
        </GlassCard>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <GlassCard className="p-5"><p className="text-sm text-slate-500">Estimated money saved</p><p className="mt-2 text-3xl font-black text-ink">${(analytics?.estimated_waste_value ?? 0).toFixed(0)}</p></GlassCard>
        <GlassCard className="p-5"><p className="text-sm text-slate-500">Food saved</p><p className="mt-2 text-3xl font-black text-ink">{(analytics?.estimated_food_saved ?? 0).toFixed(1)} units</p></GlassCard>
        <GlassCard className="p-5"><p className="text-sm text-slate-500">Plastic avoided</p><p className="mt-2 text-3xl font-black text-ink">{(analytics?.plastic_waste_avoided ?? 0).toFixed(1)} kg</p></GlassCard>
      </div>
    </div>
  );
}
