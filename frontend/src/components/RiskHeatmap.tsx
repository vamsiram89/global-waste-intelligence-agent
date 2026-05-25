import type { WastePrediction } from "../api/predictionApi";

const levelColors: Record<string, string> = {
  low: "bg-emerald-100 border-emerald-200",
  medium: "bg-amber-100 border-amber-200",
  high: "bg-orange-100 border-orange-200",
  critical: "bg-red-100 border-red-200",
};

export default function RiskHeatmap({ predictions }: { predictions: WastePrediction[] }) {
  const cells = predictions.length ? predictions.slice(0, 18) : Array.from({ length: 18 }, (_, index) => ({
    product_name: `Demo item ${index + 1}`,
    risk_level: ["low", "medium", "high", "critical"][index % 4],
    risk_score: 18 + index * 4,
  })) as WastePrediction[];

  return (
    <div className="grid grid-cols-3 gap-2 sm:grid-cols-6">
      {cells.map((item, index) => (
        <div
          key={`${item.product_name}-${index}`}
          title={`${item.product_name}: ${Math.round(item.risk_score)} risk`}
          className={`h-20 rounded-xl border p-2 transition hover:-translate-y-0.5 hover:shadow-sm ${levelColors[item.risk_level.toLowerCase()] ?? "bg-blue-50 border-blue-100"}`}
        >
          <p className="truncate text-xs font-bold text-ink">{item.product_name}</p>
          <p className="mt-3 text-lg font-black text-ink">{Math.round(item.risk_score)}</p>
        </div>
      ))}
    </div>
  );
}
