import { Loader2 } from "lucide-react";

export default function LoadingSpinner({ label = "Loading data" }: { label?: string }) {
  return (
    <div className="flex min-h-32 items-center justify-center gap-3 rounded-2xl border border-dashed border-slate-200 bg-white/70 text-sm text-slate-500">
      <Loader2 className="h-5 w-5 animate-spin text-leaf" />
      {label}
    </div>
  );
}
