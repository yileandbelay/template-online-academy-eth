
// Load the video host's iframe only when the learner presses play (a "facade"): the iframe is not part of page weight until then.
import { useState } from 'react';
export default function VideoFacade({ src }) {
  const [on, setOn] = useState(false);
  if (on) return <iframe className="video" src={src} title="Lesson video" allow="autoplay; fullscreen" style={{ border: 0, width: '100%' }} />;
  return <div className="video"><button className="btn" onClick={() => setOn(true)}>▶ Play lesson video</button></div>;
}
