import { AlertCircle, RefreshCw } from "lucide-react";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="flex flex-col gap-4 rounded-2xl border border-red-100 bg-red-50/80 p-5 text-red-800 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex gap-3">
        <AlertCircle className="mt-0.5 h-5 w-5 flex-none" />
        <div>
          <p className="font-semibold">Could not load this section</p>
          <p className="text-sm text-red-700">{message}</p>
        </div>
      </div>
      {onRetry ? (
        <button className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-2 text-sm font-semibold text-red-700 shadow-sm" onClick={onRetry}>
          <RefreshCw className="h-4 w-4" />
          Retry
        </button>
      ) : null}
    </div>
  );
}
