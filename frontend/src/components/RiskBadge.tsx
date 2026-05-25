interface RiskBadgeProps {
  level?: string;
}

const styles: Record<string, string> = {
  low: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  medium: "bg-amber-50 text-amber-700 ring-amber-200",
  high: "bg-orange-50 text-orange-700 ring-orange-200",
  critical: "bg-red-50 text-red-700 ring-red-200",
  urgent: "bg-red-50 text-red-700 ring-red-200",
  recommended: "bg-blue-50 text-blue-700 ring-blue-200",
  safe: "bg-emerald-50 text-emerald-700 ring-emerald-200",
};

export default function RiskBadge({ level = "safe" }: RiskBadgeProps) {
  const key = level.toLowerCase();
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ${styles[key] ?? styles.recommended}`}>
      {level.replace(/_/g, " ")}
    </span>
  );
}
