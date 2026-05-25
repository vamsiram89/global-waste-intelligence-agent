import { PackageCheck } from "lucide-react";
import type { InventoryItem } from "../api/inventoryApi";

interface InventoryTableProps {
  items: InventoryItem[];
  compact?: boolean;
}

export default function InventoryTable({ items, compact = false }: InventoryTableProps) {
  if (!items.length) {
    return (
      <div className="grid min-h-48 place-items-center rounded-2xl border border-dashed border-slate-200 bg-slate-50/80 p-6 text-center">
        <div>
          <PackageCheck className="mx-auto h-8 w-8 text-leaf" />
          <p className="mt-3 font-semibold text-ink">No inventory added yet</p>
          <p className="mt-1 text-sm text-slate-500">Add items to unlock predictions, recommendations, and NGO matching.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-slate-100">
        <thead>
          <tr className="text-left text-xs font-bold uppercase tracking-wide text-slate-400">
            <th className="px-4 py-3">Product</th>
            <th className="px-4 py-3">Category</th>
            <th className="px-4 py-3">Qty</th>
            <th className="px-4 py-3">Expiry</th>
            {!compact ? <th className="px-4 py-3">Demand</th> : null}
            {!compact ? <th className="px-4 py-3">Storage</th> : null}
            <th className="px-4 py-3">Value</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100 text-sm">
          {items.map((item) => (
            <tr key={item.id} className="transition hover:bg-slate-50">
              <td className="px-4 py-4 font-semibold text-ink">{item.product_name}</td>
              <td className="px-4 py-4 text-slate-600">{item.category}</td>
              <td className="px-4 py-4 text-slate-600">{item.quantity} {item.unit}</td>
              <td className="px-4 py-4 text-slate-600">{item.expiry_date}</td>
              {!compact ? <td className="px-4 py-4 capitalize text-slate-600">{item.demand_level}</td> : null}
              {!compact ? <td className="px-4 py-4 capitalize text-slate-600">{item.storage_condition}</td> : null}
              <td className="px-4 py-4 font-semibold text-slate-700">${(item.quantity * item.cost_per_unit).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
