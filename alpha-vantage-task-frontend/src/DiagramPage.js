import React from 'react';
import { Link } from 'react-router-dom';

function DiagramPage() {
  return (
    <div>
      <h1>Large Scale Video Streaming Site Diagram</h1>
      <iframe src="/large-scale-video-streaming-site.drawio.html" width="100%" height="600px" />
      <Link to="/">
        <button>Back to Home</button>
      </Link>
    </div>
  );
}

export default DiagramPage;
