export function formatDate(value) {
  if (!value) return "-";
  return new Date(value).toLocaleString();
}

export function badgeColor(risk) {
  const normalized = (risk || "").toLowerCase();
  if (normalized === "high") return "bg-red-100 text-red-700";
  if (normalized === "medium") return "bg-amber-100 text-amber-700";
  return "bg-emerald-100 text-emerald-700";
}
