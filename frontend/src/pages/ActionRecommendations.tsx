import { useEffect, useState } from "react";
import { Sparkles } from "lucide-react";
import { recommendAction, type Recommendation } from "../api/actionApi";
import { getFriendlyApiError } from "../api/apiClient";
import { getInventory, type InventoryItem } from "../api/inventoryApi";
import ErrorMessage from "../components/ErrorMessage";
import GlassCard from "../components/GlassCard";
import RecommendationCard from "../components/RecommendationCard";
import RiskBadge from "../components/RiskBadge";

export default function ActionRecommendations() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | "">("");
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getInventory().then((data) => {
      setItems(data);
      setSelectedId(data[0]?.id ?? "");
    }).catch((err) => setError(getFriendlyApiError(err).message));
  }, []);

  const generate = async () => {
    if (!selectedId) return;
    setLoading(true);
    setError("");
    try {
      setRecommendation(await recommendAction({ inventory_item_id: Number(selectedId) }));
    } catch (err) {
      setError(getFriendlyApiError(err).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="font-semibold text-leaf">Smart prevention actions</p>
        <h1 className="text-3xl font-black tracking-normal text-ink">Action Recommendations</h1>
      </div>
      {error ? <ErrorMessage message={error} /> : null}
      <div className="grid gap-6 xl:grid-cols-[0.75fr_1.25fr]">
        <GlassCard className="p-6">
          <h2 className="text-xl font-black text-ink">Generate Recommendation</h2>
          <div className="mt-5">
            <label className="label">Inventory item</label>
            <select className="field" value={selectedId} onChange={(event) => setSelectedId(Number(event.target.value))}>
              {items.map((item) => <option key={item.id} value={item.id}>{item.product_name} - {item.quantity} {item.unit}</option>)}
            </select>
          </div>
          <button className="btn-primary mt-5 w-full" disabled={!selectedId || loading} onClick={generate}><Sparkles className="h-4 w-4" /> {loading ? "Generating..." : "Generate recommendation"}</button>
          <div className="mt-6 grid gap-3">
            {["Discount suggestion", "Donation suggestion", "Reduce next order", "Recycle suggestion", "Safety warning"].map((item) => (
              <div key={item} className="flex items-center justify-between rounded-2xl bg-slate-50 p-4">
                <span className="text-sm font-semibold text-slate-700">{item}</span>
                <RiskBadge level={item.includes("Safety") ? "Needs Human Approval" : "Recommended"} />
              </div>
            ))}
          </div>
        </GlassCard>
        <div>{recommendation ? <RecommendationCard recommendation={recommendation} /> : <GlassCard className="grid min-h-72 place-items-center p-6 text-center text-slate-500">Select an inventory item to generate prevention, donation, reorder, recycle, and safety guidance.</GlassCard>}</div>
      </div>
    </div>
  );
}
