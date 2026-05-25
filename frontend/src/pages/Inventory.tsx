import { useEffect, useState } from "react";
import { Plus, RefreshCw, X } from "lucide-react";
import { addInventoryItem, getInventory, type InventoryItem, type InventoryItemPayload } from "../api/inventoryApi";
import { getFriendlyApiError } from "../api/apiClient";
import ErrorMessage from "../components/ErrorMessage";
import GlassCard from "../components/GlassCard";
import InventoryTable from "../components/InventoryTable";
import LoadingSpinner from "../components/LoadingSpinner";

const initialForm: InventoryItemPayload = {
  product_name: "Yogurt Cups",
  category: "Dairy",
  quantity: 120,
  unit: "cups",
  expiry_date: "2026-05-27",
  purchase_date: "2026-05-20",
  avg_daily_sales: 18,
  cost_per_unit: 0.8,
  storage_condition: "cold",
  demand_level: "low",
  weather_factor: "hot",
  event_factor: "none",
};

export default function Inventory() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [form, setForm] = useState(initialForm);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      setItems(await getInventory());
    } catch (err) {
      setError(getFriendlyApiError(err).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void load(); }, []);

  const update = (key: keyof InventoryItemPayload, value: string) => {
    const numberFields = ["quantity", "avg_daily_sales", "cost_per_unit"];
    setForm((current) => ({ ...current, [key]: numberFields.includes(key) ? Number(value) : value }));
  };

  const submit = async () => {
    setSaving(true);
    setError("");
    try {
      await addInventoryItem(form);
      setShowForm(false);
      await load();
    } catch (err) {
      setError(getFriendlyApiError(err).message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <p className="font-semibold text-leaf">Inventory control</p>
          <h1 className="text-3xl font-black tracking-normal text-ink">Food Safety Inventory</h1>
        </div>
        <div className="flex gap-3">
          <button className="btn-secondary" onClick={load}><RefreshCw className="h-4 w-4" /> Refresh</button>
          <button className="btn-primary" onClick={() => setShowForm(true)}><Plus className="h-4 w-4" /> Add Item</button>
        </div>
      </div>
      {error ? <ErrorMessage message={error} onRetry={load} /> : null}
      <GlassCard className="p-6">{loading ? <LoadingSpinner /> : <InventoryTable items={items} />}</GlassCard>

      {showForm ? (
        <div className="fixed inset-0 z-50 grid place-items-center bg-ink/35 p-4 backdrop-blur-sm">
          <GlassCard className="max-h-[90vh] w-full max-w-4xl overflow-y-auto p-6">
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-2xl font-black text-ink">Add Inventory Item</h2>
              <button className="grid h-10 w-10 place-items-center rounded-xl bg-slate-100" onClick={() => setShowForm(false)} aria-label="Close form"><X className="h-5 w-5" /></button>
            </div>
            <div className="grid gap-4 md:grid-cols-3">
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
            <div className="mt-6 flex justify-end gap-3">
              <button className="btn-secondary" onClick={() => setShowForm(false)}>Cancel</button>
              <button className="btn-primary" disabled={saving} onClick={submit}>{saving ? "Saving..." : "Add item"}</button>
            </div>
          </GlassCard>
        </div>
      ) : null}
    </div>
  );
}
