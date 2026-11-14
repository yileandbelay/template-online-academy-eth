import Link from 'next/link';
import EnrollButton from '../../../components/EnrollButton';
import { courses } from '../../../lib/data';
export const generateStaticParams = () => courses.map((c) => ({ slug: c.slug }));
export default async function CoursePage({ params }) {
  const { slug } = await params;
  const c = courses.find((x) => x.slug === slug);
  return (
    <article>
      <span className="badge">{c.level} · {c.hours} h</span>
      <h1>{c.title}</h1>
      <p className="muted">{c.summary}</p>
      <p>★ {c.rating} ({c.reviews} reviews) · {c.price ? `ETB ${c.price}` : 'Free'}</p>
      <EnrollButton slug={c.slug} price={c.price} />
      <h2>Syllabus</h2>
      <ul className="lessons">
        {c.lessons.map((l) => (
          <li key={l.id}>
            <span>{l.preview ? <Link href={`/lesson/${l.id}`}>{l.title}</Link> : <span className="lock">🔒 {l.title}</span>}</span>
            <span className="muted">{l.minutes} min</span>
          </li>
        ))}
      </ul>
    </article>
  );
}
