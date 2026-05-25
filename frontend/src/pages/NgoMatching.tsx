import { useEffect, useState } from "react";
import { HeartHandshake, ShieldAlert } from "lucide-react";
import { getFriendlyApiError } from "../api/apiClient";
import { getInventory, type InventoryItem } from "../api/inventoryApi";
import { getNgos, redistributeFood, type NgoPartner, type RedistributionResponse } from "../api/ngoApi";
import ErrorMessage from "../components/ErrorMessage";
import GlassCard from "../components/GlassCard";
import LoadingSpinner from "../components/LoadingSpinner";
import NgoCard from "../components/NgoCard";
import RiskBadge from "../components/RiskBadge";

export default function NgoMatching() {
  const [ngos, setNgos] = useState<NgoPartner[]>([]);
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | "">("");
  const [quantity, setQuantity] = useState(10);
  const [match, setMatch] = useState<RedistributionResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const [ngoData, inventoryData] = await Promise.all([getNgos(), getInventory()]);
      setNgos(ngoData);
      setItems(inventoryData);
      setSelectedId(inventoryData[0]?.id ?? "");
    } catch (err) {
      setError(getFriendlyApiError(err).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void load(); }, []);

  const submit = async () => {
    if (!selectedId) return;
    setError("");
    try {
      setMatch(await redistributeFood({ inventory_item_id: Number(selectedId), quantity }));
    } catch (err) {
      setError(getFriendlyApiError(err).message);
    }
  };

  const selected = items.find((item) => item.id === selectedId);

  return (
    <div className="space-y-6">
      <div>
        <p className="font-semibold text-leaf">Food redistribution network</p>
        <h1 className="text-3xl font-black tracking-normal text-ink">NGO Matching</h1>
      </div>
      <div className="flex items-start gap-3 rounded-2xl border border-blue-100 bg-blue-50 p-4 text-sm leading-6 text-blue-800">
        <ShieldAlert className="mt-0.5 h-5 w-5 flex-none" />
        <p>This MVP is a decision-support prototype. Real deployment must include food safety validation, local legal compliance, cold-chain checks, expiry verification, partner approval, and human confirmation before redistribution or pickup.</p>
      </div>
      {error ? <ErrorMessage message={error} onRetry={load} /> : null}

      <div className="grid gap-6 xl:grid-cols-[0.75fr_1.25fr]">
        <GlassCard className="p-6">
          <h2 className="text-xl font-black text-ink">Redistribution Match Form</h2>
          <div className="mt-5 space-y-4">
            <div>
              <label className="label">Inventory item</label>
              <select className="field" value={selectedId} onChange={(event) => setSelectedId(Number(event.target.value))}>
                {items.map((item) => <option key={item.id} value={item.id}>{item.product_name}</option>)}
              </select>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              <div><label className="label">Product name</label><input className="field" value={selected?.product_name ?? ""} readOnly /></div>
              <div><label className="label">Category</label><input className="field" value={selected?.category ?? ""} readOnly /></div>
              <div><label className="label">Quantity</label><input className="field" type="number" value={quantity} onChange={(event) => setQuantity(Number(event.target.value))} /></div>
              <div><label className="label">Expiry date</label><input className="field" value={selected?.expiry_date ?? ""} readOnly /></div>
              <div className="sm:col-span-2"><label className="label">Storage condition</label><input className="field" value={selected?.storage_condition ?? ""} readOnly /></div>
            </div>
            <button className="btn-primary w-full" disabled={!selectedId} onClick={submit}><HeartHandshake className="h-4 w-4" /> Match to NGO</button>
          </div>
          {match ? (
            <div className="mt-5 rounded-2xl bg-mint p-5">
              <div className="flex items-center justify-between gap-3">
                <p className="font-black text-ink">{match.ngo_name ?? "No safe match found"}</p>
                <RiskBadge level={match.status.includes("approval") ? "Needs Human Approval" : "Recommended"} />
              </div>
              <p className="mt-3 text-sm leading-6 text-slate-700">{match.message}</p>
            </div>
          ) : null}
        </GlassCard>
        <div>
          {loading ? <LoadingSpinner /> : (
            <div className="grid gap-4 md:grid-cols-2">
              {ngos.map((ngo) => <NgoCard key={ngo.id} ngo={ngo} />)}
              {!ngos.length ? <GlassCard className="p-6 text-sm text-slate-500">No partners returned by the backend yet.</GlassCard> : null}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
