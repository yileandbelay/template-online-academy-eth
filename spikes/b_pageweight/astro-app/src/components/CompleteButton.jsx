
import { useState } from 'react';
export default function CompleteButton({ id }) {
  const [done, setDone] = useState(false);
  return <button className="btn secondary" onClick={() => { setDone(true); fetch(`/api/lesson/${id}/complete`, { method: 'POST' }).catch(() => {}); }}>{done ? 'Completed ✓' : 'Mark as complete'}</button>;
}
