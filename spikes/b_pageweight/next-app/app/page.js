import Link from 'next/link';
import CourseCard from '../components/CourseCard';
import { courses } from '../lib/data';
export default function Home() {
  return (
    <>
      <section className="hero"><h1>Build skills that move your career forward.</h1>
        <p className="muted">Practical, professional training you can take anywhere.</p>
        <Link className="btn" href="/courses">Browse courses</Link></section>
      <h2>Popular courses</h2>
      <div className="grid">{courses.slice(0, 6).map((c) => <CourseCard key={c.slug} c={c} />)}</div>
    </>
  );
}
