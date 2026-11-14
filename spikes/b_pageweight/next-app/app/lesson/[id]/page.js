import CompleteButton from '../../../components/CompleteButton';
import VideoFacade from '../../../components/VideoFacade';
import { allLessons, lessonBody } from '../../../lib/data';
export const generateStaticParams = () => allLessons.map((l) => ({ id: String(l.id) }));
export default async function LessonPage({ params }) {
  const { id } = await params;
  const l = allLessons.find((x) => String(x.id) === id);
  return (
    <article className="prose">
      <p className="muted">{l.course.title}</p>
      <h1>{l.title}</h1>
      <VideoFacade src="https://iframe.mediadelivery.net/embed/0/example" />
      {lessonBody(6).map((t, i) => <p key={i}>{t}</p>)}
      <CompleteButton id={l.id} />
    </article>
  );
}
