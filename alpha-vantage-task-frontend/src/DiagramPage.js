import React from 'react';
import { Link } from 'react-router-dom';

function DiagramPage() {
  return (
    <div>
      <h1>Large Scale Video Streaming Site Diagram</h1>
      <img src="/large-scale-video-streaming-site.drawio.png" alt="Large Scale Video Streaming Site Diagram" style={{maxWidth: '100%', height: 'auto'}} />
      <Link to="/">
        <button>Back to Home</button>
      </Link>
    </div>
  );
}

export default DiagramPage;