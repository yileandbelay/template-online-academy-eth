
import { useState } from 'react';
export default function EnrollButton({ slug, price }) {
  const [busy, setBusy] = useState(false);
  return (
    <button className="btn" disabled={busy} onClick={async () => { setBusy(true); await fetch(`/api/enroll/${slug}`, { method: 'POST' }).catch(() => {}); setBusy(false); }}>
      {price ? `Enroll for ETB ${price}` : 'Enroll for free'}
    </button>
  );
}
