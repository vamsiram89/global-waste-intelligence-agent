import { useEffect, useMemo, useState } from "react";
import { Activity, RefreshCw, Wand2 } from "lucide-react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getFriendlyApiError } from "../api/apiClient";
import { type InventoryItemPayload } from "../api/inventoryApi";
import { predictAllWasteRisk, predictWasteRisk, type WastePrediction } from "../api/predictionApi";
import ErrorMessage from "../components/ErrorMessage";
import GlassCard from "../components/GlassCard";
import LoadingSpinner from "../components/LoadingSpinner";
import RiskBadge from "../components/RiskBadge";

const initialForm: InventoryItemPayload = {
  product_name: "Fresh Salad Bowls",
  category: "Prepared Food",
  quantity: 80,
  unit: "bowls",
  expiry_date: "2026-05-28",
  purchase_date: "2026-05-24",
  avg_daily_sales: 12,
  cost_per_unit: 3.5,
  storage_condition: "cold",
  demand_level: "low",
  weather_factor: "hot",
  event_factor: "none",
};

export default function WastePrediction() {
  const [form, setForm] = useState(initialForm);
  const [single, setSingle] = useState<WastePrediction | null>(null);
  const [all, setAll] = useState<WastePrediction[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadAll = async () => {
    setLoading(true);
    setError("");
    try {
      setAll(await predictAllWasteRisk());
    } catch (err) {
      setError(getFriendlyApiError(err).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void loadAll(); }, []);

  const update = (key: keyof InventoryItemPayload, value: string) => {
    const numberFields = ["quantity", "avg_daily_sales", "cost_per_unit"];
    setForm((current) => ({ ...current, [key]: numberFields.includes(key) ? Number(value) : value }));
  };

  const predictOne = async () => {
    setLoading(true);
    setError("");
    try {
      setSingle(await predictWasteRisk(form));
    } catch (err) {
      setError(getFriendlyApiError(err).message);
    } finally {
      setLoading(false);
    }
  };

  const distribution = useMemo(() => {
    const levels = ["low", "medium", "high", "critical"];
    return levels.map((level) => ({ level, count: all.filter((item) => item.risk_level.toLowerCase() === level).length }));
  }, [all]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <p className="font-semibold text-leaf">Explainable risk engine</p>
          <h1 className="text-3xl font-black tracking-normal text-ink">Waste Prediction</h1>
        </div>
        <button className="btn-secondary" onClick={loadAll}><RefreshCw className="h-4 w-4" /> Predict all stored inventory</button>
      </div>
      {error ? <ErrorMessage message={error} onRetry={loadAll} /> : null}

      <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
        <GlassCard className="p-6">
          <h2 className="text-xl font-black text-ink">Predict One Item</h2>
          <div className="mt-5 grid gap-4 md:grid-cols-2">
            {([
              ["product_name", "Product name", "text"],
              ["category", "Category", "text"],
              ["quantity", "Quantity", "number"],
              ["unit", "Unit", "text"],
              ["expiry_date", "Expiry date", "date"],
              ["purchase_date", "Purchase date", "date"],
              ["avg_daily_sales", "Average daily sales", "number"],
              ["cost_per_unit", "Cost per unit", "number"],
              ["storage_condition", "Storage condition", "text"],
              ["demand_level", "Demand level", "text"],
              ["weather_factor", "Weather factor", "text"],
              ["event_factor", "Event factor", "text"],
            ] as const).map(([key, label, type]) => (
              <div key={key}>
                <label className="label">{label}</label>
                <input className="field" type={type} value={form[key]} onChange={(event) => update(key, event.target.value)} />
              </div>
            ))}
          </div>
          <button className="btn-primary mt-6 w-full" onClick={predictOne} disabled={loading}><Wand2 className="h-4 w-4" /> Predict risk</button>
        </GlassCard>

        <div className="space-y-6">
          <GlassCard className="p-6">
            <h2 className="text-xl font-black text-ink">Risk Distribution</h2>
            <div className="mt-4 h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={distribution}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="level" />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#1E9E67" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>
          {single ? (
            <GlassCard className="p-6">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-semibold text-slate-500">Single item result</p>
                  <h3 className="mt-1 text-2xl font-black text-ink">{single.product_name}</h3>
                </div>
                <RiskBadge level={single.risk_level} />
              </div>
              <div className="mt-5 grid gap-4 sm:grid-cols-3">
                <div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs text-slate-500">Risk score</p><p className="text-2xl font-black text-ink">{single.risk_score.toFixed(0)}</p></div>
                <div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs text-slate-500">Predicted waste</p><p className="text-2xl font-black text-ink">{single.predicted_waste_quantity.toFixed(1)}</p></div>
                <div className="rounded-2xl bg-slate-50 p-4"><p className="text-xs text-slate-500">Estimated loss</p><p className="text-2xl font-black text-ink">${single.estimated_loss.toFixed(0)}</p></div>
              </div>
              <p className="mt-5 rounded-2xl bg-blue-50 p-4 text-sm leading-6 text-blue-800">{single.reason}</p>
            </GlassCard>
          ) : null}
        </div>
      </div>

      <GlassCard className="p-6">
        <h2 className="text-xl font-black text-ink">Stored Inventory Predictions</h2>
        {loading ? <div className="mt-4"><LoadingSpinner /></div> : (
          <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {all.map((item) => (
              <div key={`${item.inventory_item_id}-${item.id}`} className="rounded-2xl border border-slate-100 bg-white p-5 shadow-sm">
                <div className="flex items-start justify-between gap-3">
                  <div><p className="font-bold text-ink">{item.product_name}</p><p className="text-sm text-slate-500">{item.category}</p></div>
                  <RiskBadge level={item.risk_level} />
                </div>
                <p className="mt-4 text-sm leading-6 text-slate-600">{item.reason}</p>
              </div>
            ))}
            {!all.length ? <p className="text-sm text-slate-500">No stored predictions yet. Add inventory items first.</p> : null}
          </div>
        )}
      </GlassCard>
    </div>
  );
}
