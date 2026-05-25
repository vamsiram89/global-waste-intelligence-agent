import type { LucideIcon } from "lucide-react";
import GlassCard from "./GlassCard";

interface StatCardProps {
  title: string;
  value: string | number;
  helper: string;
  trend?: string;
  icon: LucideIcon;
  tone?: "green" | "blue" | "orange" | "red";
}

const tones = {
  green: "bg-emerald-50 text-emerald-700",
  blue: "bg-blue-50 text-blue-700",
  orange: "bg-amber-50 text-amber-700",
  red: "bg-red-50 text-red-700",
};

export default function StatCard({ title, value, helper, trend, icon: Icon, tone = "blue" }: StatCardProps) {
  return (
    <GlassCard className="p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-3 text-3xl font-bold tracking-normal text-ink">{value}</p>
          <p className="mt-2 text-xs text-slate-500">{helper}</p>
        </div>
        <div className={`rounded-2xl p-3 ${tones[tone]}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      {trend ? <p className="mt-4 text-xs font-semibold text-emerald-600">{trend}</p> : null}
    </GlassCard>
  );
}
