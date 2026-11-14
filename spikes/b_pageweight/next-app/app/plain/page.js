// A page with NO client components at all: shows the floor Next.js itself costs.
import { courses } from '../../lib/data';
export default function Plain() {
  return (<><h1>Server-only page</h1><ul>{courses.map((c) => <li key={c.slug}><a href={`/courses/${c.slug}`}>{c.title}</a></li>)}</ul></>);
}
