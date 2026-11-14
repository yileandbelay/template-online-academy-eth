import Link from 'next/link';
export default function CourseCard({ c }) {
  return (
    <article className="card">
      <span className="badge">{c.level} · {c.hours} h</span>
      <h3><Link href={`/courses/${c.slug}`}>{c.title}</Link></h3>
      <p className="muted">{c.summary}</p>
      <p>★ {c.rating} ({c.reviews}) · {c.price ? `ETB ${c.price}` : 'Free'}</p>
    </article>
  );
}
