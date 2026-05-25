import { HeartHandshake, MapPin, Phone } from "lucide-react";
import type { NgoPartner } from "../api/ngoApi";
import GlassCard from "./GlassCard";

export default function NgoCard({ ngo }: { ngo: NgoPartner }) {
  return (
    <GlassCard className="p-5">
      <div className="flex items-start gap-4">
        <div className="grid h-12 w-12 place-items-center rounded-2xl bg-emerald-50 text-leaf">
          <HeartHandshake className="h-6 w-6" />
        </div>
        <div className="min-w-0">
          <h3 className="truncate text-lg font-bold text-ink">{ngo.name}</h3>
          <p className="mt-2 flex items-center gap-2 text-sm text-slate-500"><MapPin className="h-4 w-4" /> {ngo.location}</p>
        </div>
      </div>
      <div className="mt-5 rounded-2xl bg-slate-50 p-4">
        <p className="text-xs font-bold uppercase tracking-wide text-slate-400">Accepted categories</p>
        <p className="mt-2 text-sm font-semibold text-slate-700">{ngo.accepted_categories}</p>
      </div>
      <div className="mt-4 flex items-center justify-between gap-3 text-sm">
        <span className="font-semibold text-slate-600">Capacity {ngo.capacity}</span>
        <span className="inline-flex items-center gap-2 text-slate-500"><Phone className="h-4 w-4" /> {ngo.contact}</span>
      </div>
    </GlassCard>
  );
}
