import { useEffect, useMemo, useState } from "react";
import { Apple, CircleDollarSign, PackageX, Recycle, Soup } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Cell, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getAnalyticsSummary, type AnalyticsSummary } from "../api/analyticsApi";
import { getFriendlyApiError } from "../api/apiClient";
import { predictAllWasteRisk, type WastePrediction } from "../api/predictionApi";
import ErrorMessage from "../components/ErrorMessage";
import GlassCard from "../components/GlassCard";
import LoadingSpinner from "../components/LoadingSpinner";
import StatCard from "../components/StatCard";

const colors = ["#1E9E67", "#2F80ED", "#F59E0B", "#E5484D"];

export default function Analytics() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [predictions, setPredictions] = useState<WastePrediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const [summaryData, predictionData] = await Promise.all([getAnalyticsSummary(), predictAllWasteRisk()]);
      setSummary(summaryData);
      setPredictions(predictionData);
    } catch (err) {
      setError(getFriendlyApiError(err).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { void load(); }, []);

  const categoryData = useMemo(() => {
    const totals = new Map<string, number>();
    predictions.forEach((item) => totals.set(item.category, (totals.get(item.category) ?? 0) + item.risk_score));
    return Array.from(totals, ([category, risk]) => ({ category, risk: Math.round(risk) }));
  }, [predictions]);

  const pieData = useMemo(() => ["low", "medium", "high", "critical"].map((level) => ({
    name: level,
    value: predictions.filter((item) => item.risk_level.toLowerCase() === level).length,
  })).filter((item) => item.value > 0), [predictions]);

  const trend = [
    { week: "W1", waste: 38 },
    { week: "W2", waste: 32 },
    { week: "W3", waste: 25 },
    { week: "W4", waste: 19 },
    { week: "Future", waste: 14 },
  ];

  if (loading) return <LoadingSpinner label="Loading analytics summary" />;

  return (
    <div className="space-y-6">
      <div>
        <p className="font-semibold text-leaf">Portfolio summary</p>
        <h1 className="text-3xl font-black tracking-normal text-ink">Waste Prevention Analytics</h1>
      </div>
      {error ? <ErrorMessage message={error} onRetry={load} /> : null}
      <div className="grid gap-4 md:grid-cols-2 2xl:grid-cols-5">
        <StatCard title="Estimated money saved" value={`$${(summary?.estimated_waste_value ?? 0).toFixed(0)}`} helper="Preventable waste value" icon={CircleDollarSign} tone="green" />
        <StatCard title="Food saved" value={(summary?.estimated_food_saved ?? 0).toFixed(1)} helper="Units protected" icon={Soup} tone="blue" />
        <StatCard title="Plastic avoided" value={(summary?.plastic_waste_avoided ?? 0).toFixed(1)} helper="Kg equivalent" icon={Recycle} tone="green" />
        <StatCard title="Items at risk" value={summary?.high_risk_products ?? 0} helper="High and critical exposure" icon={PackageX} tone="orange" />
        <StatCard title="Donations recommended" value={(summary?.suggested_donation_quantity ?? 0).toFixed(1)} helper="Pending approval" icon={Apple} tone="red" />
      </div>
      <div className="grid gap-6 xl:grid-cols-3">
        <GlassCard className="p-6 xl:col-span-2">
          <h2 className="text-xl font-black text-ink">Waste Risk by Category</h2>
          <div className="mt-5 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categoryData.length ? categoryData : [{ category: "Demo Dairy", risk: 72 }, { category: "Demo Produce", risk: 48 }, { category: "Demo Bakery", risk: 34 }]}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="risk" fill="#2F80ED" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
        <GlassCard className="p-6">
          <h2 className="text-xl font-black text-ink">Item Risk Levels</h2>
          <div className="mt-5 h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData.length ? pieData : [{ name: "demo", value: 1 }]} dataKey="value" nameKey="name" innerRadius={70} outerRadius={105}>
                  {(pieData.length ? pieData : [{ name: "demo", value: 1 }]).map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>
      <GlassCard className="p-6">
        <h2 className="text-xl font-black text-ink">Future Waste Trend</h2>
        <p className="mt-1 text-sm text-slate-500">Placeholder for historical forecasting once POS and ERP data are connected.</p>
        <div className="mt-5 h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trend}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="waste" stroke="#1E9E67" strokeWidth={4} dot={{ r: 5 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>
    </div>
  );
}
