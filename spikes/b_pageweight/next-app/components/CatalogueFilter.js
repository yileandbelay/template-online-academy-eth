'use client';
// A typical interactive island: client-side search and level filter over the list.
import { useMemo, useState } from 'react';
import Link from 'next/link';
export default function CatalogueFilter({ courses }) {
  const [q, setQ] = useState('');
  const [level, setLevel] = useState('');
  const shown = useMemo(() => courses.filter((c) => (!level || c.level === level) && c.title.toLowerCase().includes(q.toLowerCase())), [courses, q, level]);
  return (
    <>
      <div className="filters">
        <input aria-label="Search courses" placeholder="Search courses" value={q} onChange={(e) => setQ(e.target.value)} />
        <select aria-label="Level" value={level} onChange={(e) => setLevel(e.target.value)}>
          <option value="">All levels</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option>
        </select>
      </div>
      <div className="grid">
        {shown.map((c) => (
          <article className="card" key={c.slug}>
            <span className="badge">{c.level} · {c.hours} h</span>
            <h3><Link href={`/courses/${c.slug}`}>{c.title}</Link></h3>
            <p className="muted">{c.summary}</p>
            <p>★ {c.rating} ({c.reviews}) · {c.price ? `ETB ${c.price}` : 'Free'}</p>
          </article>
        ))}
      </div>
    </>
  );
}
