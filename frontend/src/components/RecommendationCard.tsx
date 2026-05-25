import { BadgeCheck, ShieldAlert } from "lucide-react";
import type { Recommendation } from "../api/actionApi";
import GlassCard from "./GlassCard";
import RiskBadge from "./RiskBadge";

export default function RecommendationCard({ recommendation }: { recommendation: Recommendation }) {
  return (
    <GlassCard className="p-6">
      <div className="flex items-start justify-between gap-4">
        <div className="flex gap-4">
          <div className="grid h-12 w-12 place-items-center rounded-2xl bg-mint text-leaf">
            <BadgeCheck className="h-6 w-6" />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-500">{recommendation.product_name ?? `Item #${recommendation.inventory_item_id}`}</p>
            <h3 className="mt-1 text-xl font-bold text-ink">{recommendation.action_type.replace(/_/g, " ")}</h3>
          </div>
        </div>
        <RiskBadge level={recommendation.urgency || "Recommended"} />
      </div>
      <p className="mt-5 leading-7 text-slate-600">{recommendation.action_message}</p>
      <div className="mt-5 flex items-start gap-3 rounded-2xl bg-blue-50 p-4 text-sm text-blue-800">
        <ShieldAlert className="mt-0.5 h-5 w-5 flex-none" />
        <p>Needs Human Approval before redistribution, pickup, or external partner action.</p>
      </div>
    </GlassCard>
  );
}
